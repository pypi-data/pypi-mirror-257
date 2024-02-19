import random
from genomkit import GRegion
import copy
import numpy as np
from .io import load_BED


###########################################################################
# GRegions
###########################################################################
class GRegions:
    """
    GRegions module

    This module contains functions and classes for working with a collection of
    genomic regions. It provides utilities for handling and analyzing the
    interactions of many genomic coordinates.
    """
    def __init__(self, name: str = "", load: str = ""):
        """Create an empty GRegions object. If a path to a BED file is defined
        in "load", all the regions will be loaded.

        :param name: Name of this GRegions, defaults to ""
        :type name: str, optional
        :param load: Path to a BED file, defaults to ""
        :type load: str, optional
        """
        self.elements = []
        self.sorted = False
        self.name = name
        if load:
            self.load(load)

    def __len__(self):
        """Return the number of regions in this GRegions.

        :return: Number of regions
        :rtype: int
        """
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def add(self, region):
        """Append a GRegion at the end of the elements of GRegions.

        :param region: A GRegion
        :type region: GRegion
        """
        self.elements.append(region)
        self.sorted = False

    def load(self, filename: str):
        """Load a BED file into the GRegions.

        :param filename: Path to the BED file
        :type filename: str
        """
        regions = load_BED(filename=filename)
        self.elements = regions.elements
        self.sorted = False

    def write(self, filename: str):
        """Write a BED file.

        :param filename: Path to the BED file
        :type filename: str
        """
        with open(filename, "w") as f:
            for region in self.elements:
                print(region.bed_entry(), file=f)

    def sort(self, key=None, reverse: bool = False):
        """Sort elements by criteria defined by a GenomicRegion.

        :param key: Given the key for comparison.
        :type key: str
        :param reverse: Reverse the sorting result.
        :type reverse: bool
        """
        if key:
            self.elements.sort(key=key, reverse=reverse)
        else:
            self.elements.sort()
            self.sorted = True

    def get_sequences(self, unique: bool = False):
        """Return all chromosomes.

        :param unique: Only the unique names.
        :type unique: bool
        :return: A list of all chromosomes.
        :rtype: list
        """
        res = [r.sequence for r in self]
        if unique:
            res = list(set(res))
            res.sort()
        return res

    def get_names(self, unique: bool = False):
        """Return a list of all region names. If the name is None,
        it return the region string.

        :return: A list of all regions' names.
        :rtype: list
        """
        names = [r.name if r.name else r.toString() for r in self]
        if unique:
            names = list(set(names))
            names.sort()
        return names

    def extend(self, upstream: int = 0, downstream: int = 0,
               strandness: bool = False, inplace: bool = True):
        """Perform extend step for every element. The extension length can also
        be negative values which shrinkages the regions.

        :param upstream: Define how many bp to extend toward upstream
                         direction.
        :type upstream: int
        :param downstream: Define how many bp to extend toward downstream
                          direction.
        :type downstream: int
        :param strandness: Define whether strandness is considered.
        :type strandness: bool
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object.
        :type inplace: bool
        :return: None or a GRegions object
        """
        if inplace:
            for region in self.elements:
                region.extend(upstream=upstream,
                              downstream=downstream,
                              strandness=strandness,
                              inplace=True)
        else:
            output = GRegions(name=self.name)
            for region in self.elements:
                r = region.extend(upstream=upstream,
                                  downstream=downstream,
                                  strandness=strandness,
                                  inplace=False)
                output.add(r)
            return output

    def extend_fold(self, upstream: float = 0.0, downstream: float = 0.0,
                    strandness: bool = False, inplace: bool = True):
        """Perform extend step for every element. The extension length can also
        be negative values which shrinkages the regions.

        :param upstream: Define the percentage of the region length to extend
                         toward upstream direction.
        :type upstream: float
        :param downstream: Define the percentage of the region length to extend
                           toward downstream direction.
        :type downstream: float
        :param strandness: Define whether strandness is considered.
        :type strandness: bool
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object..
        :type inplace: bool
        :return: None
        """
        if inplace:
            for region in self.elements:
                region.extend_fold(upstream=upstream,
                                   downstream=downstream,
                                   strandness=strandness,
                                   inplace=True)
        else:
            output = GRegions(name=self.name)
            for region in self.elements:
                r = region.extend_fold(upstream=upstream,
                                       downstream=downstream,
                                       strandness=strandness,
                                       inplace=False)
                output.add(r)
            return output

    def intersect_python(self, target, mode: str = "OVERLAP",
                         rm_duplicates: bool = False):
        """Return a GRegions for the intersections between the two given
        GRegions objects. There are three modes for overlapping:

        *mode = "OVERLAP"*

            Return a new GRegions including only the overlapping regions
            with target GRegions.

            .. note:: it will merge the regions.

            ::

                self       ----------              ------
                target            ----------                    ----
                Result            ---

        *mode = "ORIGINAL"*

            Return the regions of original GenomicRegionSet which have any
            intersections with target GRegions.

            ::

                self       ----------              ------
                target          ----------                    ----
                Result     ----------

        *mode = "COMP_INCL"*

            Return region(s) of the GenomicRegionSet which are 'completely'
            included by target GRegions.

            ::

                self        -------------             ------
                target              ----------      ---------------       ----
                Result                                ------

        :param target: A target GRegions for finding overlaps.
        :type target: GRegions
        :param mode: The mode should be one of the followings: "OVERLAP",
                     "ORIGINAL", or "COMP_INCL".
        :type mode: str
        :param rm_duplicates: Define whether remove the duplicates.
        :type rm_duplicates: bool
        :return: A GRegions.
        :rtype: GRegions
        """
        new_regions = GRegions(self.name)
        if len(self) == 0 or len(target) == 0:
            return new_regions
        else:
            a = copy.deepcopy(self)
            b = copy.deepcopy(target)
            if not a.sorted:
                a.sort()
            if not b.sorted:
                b.sort()
            if mode == "OVERLAP":
                a.merge()
                b.merge()

            iter_a = iter(a)
            s = next(iter_a)
            last_j = len(b) - 1
            j = 0
            cont_loop = True
            pre_inter = 0
            cont_overlap = False
            # OVERLAP ###############################
            if mode == "OVERLAP":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        new_regions.add(GRegion(sequence=s.sequence,
                                                start=max(s.start, b[j].start),
                                                end=min(s.end, b[j].end),
                                                name=s.name,
                                                orientation=s.orientation,
                                                data=s.data))
                        if not cont_overlap:
                            pre_inter = j
                        if j == last_j:
                            try:
                                s = next(iter_a)
                            except StopIteration:
                                cont_loop = False
                        else:
                            j += 1
                        cont_overlap = True

                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                            if s.sequence == b[j].sequence and pre_inter > 0:
                                j = pre_inter
                            cont_overlap = False
                        except StopIteration:
                            cont_loop = False

                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                            cont_overlap = False
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False

            # ORIGINAL ###############################
            if mode == "ORIGINAL":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        new_regions.add(s)
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
            # COMP_INCL ###############################
            if mode == "COMP_INCL":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        if s.start >= b[j].start and s.end <= b[j].end:
                            new_regions.add(s)
                        if not cont_overlap:
                            pre_inter = j
                        if j == last_j:
                            try:
                                s = next(iter_a)
                            except StopIteration:
                                cont_loop = False
                        else:
                            j += 1
                        cont_overlap = True

                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                            if s.sequence == b[j].sequence and pre_inter > 0:
                                j = pre_inter
                            cont_overlap = False
                        except StopIteration:
                            cont_loop = False

                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                            cont_overlap = False
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False

            # if rm_duplicates:
            new_regions.remove_duplicates()
            # new_regions.sort()
            return new_regions

    def remove_duplicates(self, sort: bool = True):
        """
        Remove any duplicate regions (sorted, by default).
        """
        self.elements = list(set(self.elements))
        if sort:
            self.sort()

    def merge(self, by_name: bool = False, strandness: bool = False,
              inplace: bool = False):
        """Merge the regions within the GRegions object.

        :param name_distinct: Define whether to merge regions by name. If True,
                              only the regions with the same name are merged.
        :type name_distinct: bool
        :param strandness: Define whether to merge the regions according to
                           strandness.
        :type strandness: bool
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object..
        :type inplace: bool
        :return: None or a GRegions.
        :rtype: GRegions
        """
        if not self.sorted:
            self.sort()
        if len(self.elements) in [0, 1]:
            if inplace:
                return self
            else:
                pass
        else:
            res = GRegions(name=self.name)
            prev_region = self.elements[0]
            if not by_name and not strandness:
                for cur_region in self.elements[1:]:
                    if prev_region.overlap(cur_region):
                        prev_region.start = min(prev_region.start,
                                                cur_region.start)
                        prev_region.end = max(prev_region.end,
                                              cur_region.end)
                    else:
                        res.add(prev_region)
                        prev_region = cur_region
                res.add(prev_region)
            elif by_name and not strandness:
                for cur_region in self.elements[1:]:
                    if (prev_region.overlap(cur_region)) and \
                       (prev_region.name == cur_region.name):
                        prev_region.start = min(prev_region.start,
                                                cur_region.start)
                        prev_region.end = max(prev_region.end,
                                              cur_region.end)
                    else:
                        res.add(prev_region)
                        prev_region = cur_region
                res.add(prev_region)

            elif not by_name and strandness:
                for cur_region in self.elements[1:]:
                    if (prev_region.overlap(cur_region)) and \
                       (prev_region.orientation == cur_region.orientation):
                        prev_region.start = min(prev_region.start,
                                                cur_region.start)
                        prev_region.end = max(prev_region.end,
                                              cur_region.end)
                    else:
                        res.add(prev_region)
                        prev_region = cur_region
                res.add(prev_region)

            elif by_name and strandness:
                for cur_region in self.elements[1:]:
                    if (prev_region.overlap(cur_region)) and \
                       (prev_region.name == cur_region.name) and \
                       (prev_region.orientation == cur_region.orientation):
                        prev_region.start = min(prev_region.start,
                                                cur_region.start)
                        prev_region.end = max(prev_region.end,
                                              cur_region.end)
                    else:
                        res.add(prev_region)
                        prev_region = cur_region
                res.add(prev_region)

            if inplace:
                self.elements = res.elements
            else:
                return res

    def sampling(self, size: int, seed: int = None):
        """Return a sampling of the elements with a sampling number.

        :param size: Sampling number
        :type size: int
        :param seed: Seed for randomness, defaults to None
        :type seed: int, optional
        :return: Sampling regions
        :rtype: GRegions
        """
        if seed:
            random.seed(seed)
        res = GRegions(name="sampling")
        sampling = random.sample(range(len(self)), size)
        for i in sampling:
            res.add(self.elements[i])
        return res

    def split(self, ratio: float, size: int = None, seed: int = None):
        """Split the elements into two GRegions with the defined sizes.

        :param ratio: Define the ratio for splitting
        :type ratio: float, optional
        :param size: Define the size of the first GRegions, defaults to None
        :type size: int, optional
        :param seed: _description_, defaults to None
        :type seed: int, optional
        :return: Two GRegions
        :rtype: GRegions
        """
        if seed:
            random.seed(seed)
        if size:
            sampling = random.sample(range(len(self)), size)
        elif ratio and not size:
            size = int(len(self)*ratio)
            sampling = random.sample(range(len(self)), size)
        a = GRegions(name=self.name+"_split1")
        b = GRegions(name=self.name+"_split2")
        for i in range(len(self)):
            if i in sampling:
                a.add(self.elements[i])
            else:
                b.add(self.elements[i])
        return a, b

    def close_regions(self, target, max_dis=10000):
        """Return a new GRegions including the region(s) of target which are
        closest to any self region.
        If there are intersection, return False.

        :param target: the GRegions which to compare with
        :type target: GRegions
        :param max_dis: maximum distance, defaults to 10000
        :type max_dis: int, optional
        :return: Close regions
        :rtype: GRegions
        """
        if not self.sorted:
            self.sort()
        if not target.sorted:
            target.sort()

        extended_regions = self.extend(upstream=max_dis, downstream=max_dis,
                                       inplace=False)
        potential_targets = target.intersect(extended_regions,
                                             mode="ORIGINAL")
        return potential_targets

    def get_elements_by_seq(self, sequence: str, orientation: str = None):
        if orientation is None:
            regions = GRegions(name=sequence)
            regions.elements = [r for r in self.elements
                                if r.sequence == sequence]
        else:
            regions = GRegions(name=sequence+" "+orientation)
            regions.elements = [r for r in self.elements
                                if r.sequence == sequence and
                                r.orientation == orientation]
        return regions

    def get_array_by_seq(self, sequence: str, orientation: str = None):
        regions = self.get_elements_by_seq(sequence=sequence,
                                           orientation=orientation)
        max_position = max([r.end for r in regions])
        bool_array = np.full(max_position, False, dtype=bool)
        for r in regions:
            bool_array[r.start:r.end] = True
        return bool_array

    def intersect_array(self, target, strandness: bool = False):
        def find_intersects(orientation):
            array_1 = self.get_array_by_seq(sequence=seq,
                                            orientation=orientation)
            array_2 = target.get_array_by_seq(sequence=seq,
                                              orientation=orientation)
            array_1, array_2 = make_array_same_length(array_1, array_2)
            result_array = array_1 & array_2
            # Find the indices where the value changes
            indices = np.where(np.diff(result_array))[0] + 1
            # Group consecutive indices into tuples
            ranges = [(indices[i - 1], indices[i])
                      for i in range(1, len(indices), 2)]
            return ranges

        def make_array_same_length(array_1, array_2):
            # Find the maximum length of the two arrays
            max_length = max(len(array_1), len(array_2))
            # Extend the shorter array by filling it with False values
            if len(array_1) < max_length:
                array_1 = np.append(array_1,
                                    [False] * (max_length - len(array_1)))
            elif len(array_2) < max_length:
                array_2 = np.append(array_2,
                                    [False] * (max_length - len(array_2)))
            return array_1, array_2

        res = GRegions()
        list_seq_self = self.get_sequences(unique=True)
        list_seq_target = target.get_sequences(unique=True)
        common_seq = [seq for seq in list_seq_self if seq in list_seq_target]
        for seq in common_seq:
            if strandness:
                # positive
                ranges_pos = find_intersects(orientation="+")
                ranges_neg = find_intersects(orientation="-")
                ranges = ranges_pos + ranges_neg
            else:
                ranges = find_intersects(orientation=None)
            for pair in ranges:
                res.add(GRegion(sequence=seq, start=pair[0], end=pair[1],
                                name=""))
        return res

    def overlap_count(self, target):
        intersect = self.intersect_python(target, mode="ORIGINAL")
        return len(intersect)

    