import qiime2.plugin
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import SequencesWithQuality
from q2_types.feature_table import Frequency, RelativeFrequency

import q2_humann3


plugin = qiime2.plugin.Plugin(
    name='humann3',
    version=q2_humann3.__version__,
    website='http://huttenhower.sph.harvard.edu/humann2',
    package='q2_humann3',
    user_support_text=("To get help with HUMAnN3, please post a question to "
                       "the HUMAnN Google Group form: "
                       "https://groups.google.com/forum/#!forum/humann-users"),
    citation_text=None
)


plugin.methods.register_function(
    function=q2_humann3.run,
    inputs={'demultiplexed_seqs': SampleData[SequencesWithQuality]},
    parameters={'threads': qiime2.plugin.Int},
    name='Characterize samples using HUMAnN3',
    outputs=[('genefamilies', FeatureTable[Frequency]),
             ('pathcoverage', FeatureTable[RelativeFrequency]),
             ('pathabundance', FeatureTable[RelativeFrequency])],
    description='Execute the HUMAnN3'
)
