prediction_set_id = 'ddg_monomer_16-zemu-betanov15v2' # This should be a valid filename
protocol_name = 'ddg_mon16-betanov15v2'

user_dataset_name = 'AllBindingAffinity'
tagged_subset = 'ZEMu'
prediction_set_description = 'ddg_monomer_16 on ZEMU with beta November 2015 score function, and more recent Rosetta checkout with bugfixes'
extra_flags = ['-beta_nov15']

# score_method_id = 7 # rescore with interface weights score method (this is probably best...need to benchmark more)
# score_method_id = 8 # rescore with talaris weights score method
score_method_ids = [10]

# Prediction set analysis
prediction_set_credit = 'Kyle Barlow'
take_lowests = [3, 50]#, 10, 20, 30, 40, 50]
expectn = 40
use_existing_benchmark_data = True
allow_missing_case_failures = True
