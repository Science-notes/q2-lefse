# ----------------------------------------------------------------------------
# Copyright (c) 2023-, zd200572 & QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import SemanticType, model
from q2_types.sample_data import SampleData


OTUTable = SemanticType('OTUTable', variant_of=SampleData.field['type'])


class OTUTableFormat(model.TextFileFormat):
    def validate(*args):
        pass


OTUTableDirFmt = model.SingleFileDirectoryFormat(
    'OTUTableDirFmt', 'otu.txt', OTUTableFormat)
