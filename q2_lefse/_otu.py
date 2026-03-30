# ----------------------------------------------------------------------------
# Copyright (c) 2023-, zd200572 & QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import SemanticType, ValidationError, model
from q2_types.sample_data import SampleData


OTUTable = SemanticType('OTUTable', variant_of=SampleData.field['type'])


class OTUTableFormat(model.TextFileFormat):
    def validate(self, level):
        with open(str(self), 'r', encoding='utf-8') as fh:
            header = fh.readline().strip('\n')
            if not header:
                raise ValidationError('OTU table is empty.')
            if '\t' not in header:
                raise ValidationError('OTU table must be tab-delimited.')

            second = fh.readline().strip('\n')
            if not second:
                raise ValidationError('OTU table must include at least one feature row.')


OTUTableDirFmt = model.SingleFileDirectoryFormat(
    'OTUTableDirFmt', 'otu.txt', OTUTableFormat)
