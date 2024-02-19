import numpy as np
import pandas as pd
import pyBigWig
import pyranges as pr
import xarray as xr
import zarr
from scipy.sparse import csr_matrix


class CutSitesZarr(xr.Dataset):
    """Class to read cutsite zarr file and provide functionality to convert single cell cutsite data to pseudobulk coverage data."""

    def __init__(self, zarr_path) -> None:
        ds = xr.open_zarr(zarr_path)
        super().__init__(data_vars=ds.data_vars, coords=ds.coords, attrs=ds.attrs)

        self.barcode_to_idx = ds["barcode_map"].to_pandas()
        self.idx_to_barcode = pd.Series({i: b for b, i in self.barcode_to_idx.items()})
        self.chrom_offsets = ds["chrom_offset"].to_pandas()
        self.genome_total_length = self.chrom_offsets["size"].sum()
        self._zarr_compressor = zarr.Blosc(cname="zstd", clevel=3, shuffle=zarr.Blosc.SHUFFLE)

    def get_barcodes_idx(self, barcodes):
        """Get the index of the barcodes in the barcode_map."""
        if np.issubdtype(barcodes.dtype, np.integer):
            return barcodes

        use_barcodes_idx = self.barcode_to_idx[self.barcode_to_idx.index.isin(barcodes)].values
        return use_barcodes_idx

    def _get_barcodes_sites_count(self, barcodes):
        use_idx = self.get_barcodes_idx(barcodes)
        if use_idx.size == 0:
            return pd.Series(dtype=np.uint32)

        # cutsite chunks
        site_chunks = self["cutsite"].chunks[0]
        chunk_boarders = [0] + list(np.cumsum(site_chunks))

        total_cutsites = []
        for _i in range(len(site_chunks)):
            chunk_start = chunk_boarders[_i]
            chunk_end = chunk_boarders[_i + 1]

            # first, select barcode idx bool array
            use_chunk_sites = np.isin(self["cutsite"][chunk_start:chunk_end, 0], use_idx)
            # second, load actual cutsite global positions with the bool array
            use_chunk_cutsites = self["cutsite"][chunk_start:chunk_end, 1][use_chunk_sites].values
            total_cutsites.append(use_chunk_cutsites)

        pos, counts = np.unique(np.concatenate(total_cutsites), return_counts=True)
        return pos, counts.astype("uint32")

    def _get_barcode_category_sites_count(self, barcodes_category):
        """
        Get the cutsite counts for multiple barcodes categories provided as a pandas series.

        Parameters
        ----------
        barcodes_category : pd.Series
            A pandas series with barcode as index and category as values.

        Returns
        -------
        dict
            A dictionary with category as keys and a tuple of numpy arrays (position, count) as values.
        """
        # convert barcode idx to category
        idx_to_category = barcodes_category.copy()
        idx_to_category.index = idx_to_category.index.map(self.barcode_to_idx)
        idx_to_category = idx_to_category.astype("str").astype("category")

        use_idx = self.get_barcodes_idx(barcodes_category.index)
        if use_idx.size == 0:
            return {cat: (np.array([]), np.array([])) for cat in barcodes_category.astype(str).unique()}

        # cutsite chunks
        site_chunks = self["cutsite"].chunks[0]
        chunk_boarders = [0] + list(np.cumsum(site_chunks))

        total_cutsites = {cat: [] for cat in barcodes_category.astype(str).unique()}
        for _i in range(len(site_chunks)):
            chunk_start = chunk_boarders[_i]
            chunk_end = chunk_boarders[_i + 1]

            # first, select barcode idx bool array
            use_chunk_sites = np.isin(self["cutsite"][chunk_start:chunk_end, 0], use_idx)
            # second, load actual cutsite global positions with the bool array
            use_chunk_cutsites = self["cutsite"][chunk_start:chunk_end, :][use_chunk_sites].to_pandas()
            # third, group by category and append to the total_cutsites
            for group, group_global_pos in use_chunk_cutsites["global_pos"].groupby(
                use_chunk_cutsites["barcode"].map(idx_to_category)
            ):
                total_cutsites[group].append(group_global_pos.values)

        # convert the list of arrays to a single array and count the unique values
        total_cutsites = {
            cat: np.unique(np.concatenate(sites), return_counts=True) for cat, sites in total_cutsites.items()
        }
        return total_cutsites

    def _sites_count_to_coverage_zarr(self, pos, counts, zarr_path, chunk_size):
        """Convert sites count to coverage."""
        coverage = np.zeros(self.genome_total_length, dtype=np.uint32)
        coverage[pos] = counts

        # cut the coverage to the chromosome lengths and store in zarr
        root = zarr.group(store=zarr_path, overwrite=True)

        for chrom, (
            global_start,
            global_end,
            _,
        ) in self.chrom_offsets.iterrows():
            root.create_dataset(
                f"chrs/{chrom}",
                data=coverage[global_start:global_end],
                chunks=chunk_size,
                compressor=self._zarr_compressor,
            )
        return

    def _category_sites_count_to_coverage_zarr(self, total_cutsites, zarr_path, chunk_size=20000000):
        """
        Save the cutsite counts for multiple categories to zarr file.

        The data will be separated by chromosome, and each chromosome will be saved as a separate dataset in the zarr file.
        For each chromosome, the data will be a category-by-position matrix, chunked by (1, chunk_size).
        """
        # cut the coverage to the chromosome lengths and store in zarr
        root = zarr.group(store=zarr_path, overwrite=True)

        n_categories = len(total_cutsites)
        # create empty datasets for each chromosome
        for chrom, size in self.chrom_offsets["size"].items():
            root.create_dataset(
                f"chrs/{chrom}",
                shape=(n_categories, size),
                chunks=(1, chunk_size),
                dtype=np.uint32,
                compressor=self._zarr_compressor,
            )

        # save each category to the zarr file
        cat_to_idx = {}
        for idx, (cat, (pos, counts)) in enumerate(total_cutsites.items()):
            cat_to_idx[cat] = idx
            coverage = np.zeros(self.genome_total_length, dtype=np.uint32)
            coverage[pos] = counts
            for chrom, (
                global_start,
                global_end,
                _,
            ) in self.chrom_offsets.iterrows():
                root[f"chrs/{chrom}"][idx, :] = coverage[global_start:global_end]
        return

    def _sites_count_to_bigwig(self, pos, counts, bigwig_path, resolution_bp=1):
        """Convert sites count to bigwig."""
        coverage = np.zeros(self.genome_total_length, dtype=np.uint32)
        coverage[pos] = counts

        with pyBigWig.open(bigwig_path, "w") as bw:
            header = list(self.chrom_offsets["size"].items())
            bw.addHeader(header)
            for chrom, (
                global_start,
                global_end,
                _,
            ) in self.chrom_offsets.iterrows():
                chrom_coverage = coverage[global_start:global_end]
                chrom_pos = np.where(chrom_coverage > 0)[0]
                chrom_counts = chrom_coverage[chrom_pos]
                if resolution_bp > 1:
                    resolution_bp = int(resolution_bp)
                    pos_counts = pd.Series(chrom_counts, index=chrom_pos // resolution_bp * resolution_bp)
                    pos_counts = pos_counts.groupby(pos_counts.index).sum()
                    chrom_pos = pos_counts.index.values
                    chrom_counts = pos_counts.values

                bw.addEntries(
                    chrom,
                    chrom_pos,
                    values=chrom_counts.astype("float32"),
                    span=resolution_bp,
                )
        return

    def dump_barcodes_coverage(self, barcodes, zarr_path, chunk_size=50000000):
        """Get the coverage for the barcodes and save to zarr file."""
        pos, counts = self._get_barcodes_sites_count(barcodes)
        self._sites_count_to_coverage_zarr(pos, counts, zarr_path, chunk_size)
        return

    def dump_barcodes_category_coverage(self, barcodes_category, zarr_path, chunk_size=50000000):
        """Get the coverage for the barcodes and save to zarr file."""
        total_cutsites = self._get_barcode_category_sites_count(barcodes_category)
        self._category_sites_count_to_coverage_zarr(total_cutsites, zarr_path, chunk_size)
        return

    def dump_barcodes_bigwig(self, barcodes, bigwig_path, resolution_bp=1):
        """Get the coverage for the barcodes and save to bigwig file."""
        pos, counts = self._get_barcodes_sites_count(barcodes)
        self._sites_count_to_bigwig(pos, counts, bigwig_path, resolution_bp)
        return

    def _pos_df_to_chrom_bed(self, cutsites_df):
        chrom_pos = cutsites_df["global_pos"].astype("int").copy()
        chrom_count = np.zeros_like(chrom_pos, dtype="uint16")
        for _, size in self.chrom_offsets["size"].items():
            _temp_pos = chrom_pos - size
            is_pos = _temp_pos > 0
            chrom_pos = np.where(is_pos, _temp_pos, chrom_pos)
            chrom_count += is_pos.astype("uint16")
        idx_to_chrom = pd.Series(dict(enumerate(self.chrom_offsets.index)), dtype="category")
        pos_bed = pd.DataFrame({"Chromosome": chrom_count, "Start": chrom_pos, "End": chrom_pos + 1})
        pos_bed["Chromosome"] = pos_bed["Chromosome"].map(idx_to_chrom)
        pos_bed["Cell"] = cutsites_df["barcode"]
        return pos_bed

    def count_regions(self, bed_path, use_barcodes=None):
        """
        Count the number of cutsite overlaps with the regions in the bed file.

        Parameters
        ----------
        bed_path : str
            The path to the bed file with the regions to count overlaps with.
        use_barcodes : np.array, optional
            The barcodes to use for the counting. If None, all barcodes will be used.

        Returns
        -------
        csr_matrix, pd.Index, pd.Index
            The count of cutsite overlaps with the regions in the bed file, the row names and the column names.
        """
        import ray

        if not ray.is_initialized():
            ray.init(address="auto")

        if use_barcodes is None:
            use_barcodes = self.get_index("barcode")
        use_idx = self.get_barcodes_idx(use_barcodes)

        region_bed = pr.read_bed(bed_path)
        region_bed_remote = ray.put(region_bed)

        @ray.remote
        def _count(cell, cell_bed):
            _region_bed = ray.get(region_bed_remote)
            count = _region_bed.count_overlaps(cell_bed, keep_nonoverlapping=True).df.iloc[:, -1].values
            nnz_idx = np.where(count)[0]
            nnz_count = count[nnz_idx]
            count = pd.Series(nnz_count.astype("uint32"), index=nnz_idx.astype("uint32"))
            return cell, count

        # cutsite chunks
        site_chunks = self["cutsite"].chunks[0]
        chunk_boarders = [0] + list(np.cumsum(site_chunks))

        futures = []
        for _i in range(len(site_chunks)):
            chunk_start = chunk_boarders[_i]
            chunk_end = chunk_boarders[_i + 1]
            # first, select barcode idx bool array
            use_chunk_sites = np.isin(self["cutsite"][chunk_start:chunk_end, 0], use_idx)
            if use_chunk_sites.sum() == 0:
                continue

            # second, load actual cutsite global positions with the bool array
            use_chunk_cutsites = self["cutsite"][chunk_start:chunk_end, :][use_chunk_sites].to_pandas()

            pos_bed = self._pos_df_to_chrom_bed(use_chunk_cutsites)

            for cell, cell_bed in pos_bed.groupby("Cell"):
                cell_bed = pr.PyRanges(cell_bed)
                futures.append(_count.remote(cell, cell_bed))

        all_data = {}
        for future in ray.get(futures):
            cell, cell_count = future
            if cell in all_data:
                all_data[cell] = pd.concat([all_data[cell], cell_count])
            else:
                all_data[cell] = cell_count

        # init empty csr matrix for final data
        n_regions = region_bed.df.shape[0]
        n_cells = len(all_data)
        data, indices, indptr = [], [], [0]
        for _, cell_barcode in enumerate(use_barcodes):
            cell_idx = self.barcode_to_idx[cell_barcode]
            cell_count = all_data[cell_idx].sort_index()
            data.extend(cell_count.values)
            indices.extend(cell_count.index)
            indptr.append(indptr[-1] + len(cell_count))
        csr_data = csr_matrix((data, indices, indptr), shape=(n_cells, n_regions))

        row_names = pd.Index(use_barcodes, name="cell")
        col_names = pd.Index(region_bed.df["Name"].values, name="region")
        return csr_data, row_names, col_names
