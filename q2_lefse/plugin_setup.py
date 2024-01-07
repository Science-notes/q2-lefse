import qiime2.plugin
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import SequencesWithQuality
from q2_types.feature_table import Frequency, RelativeFrequency, FeatureTable

import q2_lefse


plugin = qiime2.plugin.Plugin(
    name='lefse',
    version=q2_lefse.__version__,
    website='http://huttenhower.sph.harvard.edu/humann2',
    package='q2_lefse',
    user_support_text=("To get help with lefse, please post a question to "
                       "the HUMAnN Google Group form: "
                       "https://groups.google.com/forum/#!forum/humann-users"),
    citation_text=None
)


plugin.methods.register_function(
    function=q2_lefse.run,
    inputs={'demultiplexed_seqs': SampleData[SequencesWithQuality]},
    parameters={'threads': qiime2.plugin.Int},
    name='Linear discriminant analysis Effect Size analysis using lefse',
    outputs=[('genefamilies', FeatureTable[Frequency]),
             ('pathcoverage', FeatureTable[RelativeFrequency]),
             ('pathabundance', FeatureTable[RelativeFrequency])],
    description='Execute the lefse'
)

plugin.visualizers.register_function(
    function=q2_lefse.run,
    inputs={'demultiplexed_seqs': SampleData[SequencesWithQuality]},
    parameters={'threads': qiime2.plugin.Int},
    name='Linear discriminant analysis Effect Size analysis using lefse',
    outputs=[('genefamilies', FeatureTable[Frequency]),
             ('pathcoverage', FeatureTable[RelativeFrequency]),
             ('pathabundance', FeatureTable[RelativeFrequency])],
    description='Execute the lefse'
)
