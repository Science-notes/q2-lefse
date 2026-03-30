import qiime2.plugin

import q2_lefse
from q2_lefse._otu import OTUTable, OTUTableDirFmt


plugin = qiime2.plugin.Plugin(
    name='lefse',
    version=q2_lefse.__version__,
    website='https://github.com/Science-notes/q2-lefse',
    package='q2_lefse',
    user_support_text=(
        'To get help with lefse, please post a question to '
        'https://github.com/Science-notes/q2-lefse'
    ),
    citation_text=None,
)

plugin.register_semantic_types(OTUTable)
plugin.register_formats(OTUTableDirFmt)
plugin.register_semantic_type_to_format(OTUTable, artifact_format=OTUTableDirFmt)

common_parameters = {
    'class_id': qiime2.plugin.Int,
    'subclass_id': qiime2.plugin.Int,
    'subject_id': qiime2.plugin.Int,
    'normalization': qiime2.plugin.Int,
    'lda_threshold': qiime2.plugin.Float,
    'wilcoxon_alpha': qiime2.plugin.Float,
    'kruskal_alpha': qiime2.plugin.Float,
    'command_prefix': qiime2.plugin.Str,
}

plugin.methods.register_function(
    function=q2_lefse.run,
    inputs={'otu_table': OTUTable},
    parameters=common_parameters,
    name='Run LEfSe differential analysis',
    outputs=[('lefse_results', OTUTable)],
    description='Execute LEfSe (format + run) and produce the LEfSe result table.',
)

plugin.visualizers.register_function(
    function=q2_lefse.visualize,
    inputs={'otu_table': OTUTable},
    parameters=common_parameters,
    name='Visualize LEfSe output',
    description='Run LEfSe and generate standard LEfSe plots and result table.',
)
