#!/usr/bin/python

import adapter_trimming
import alignment_gotcloud
import filtering
import re
import os
import sys

if len(sys.argv)!=2:
	print('Usage: python command.py config_file')
	print('Refer to https://github.com/YuhuaZhang1995/ATACseq_pipeline for more help')
	sys.exit(2)

config_file=open(sys.argv[1])
commands={}
func_call=[]
for ele in config_file:
	if (re.search('--',ele)):
		ele=re.sub('--','',ele)
		tmp=ele.rstrip().split(' ')
		commands[tmp[0]]=tmp[1:]
	elif (re.search('##',ele)):
		ele=re.sub('##','',ele)
		tmp=ele.rstrip().split(' ')
		func_call.append(tmp[0])
config_file.close() 

#first deal with the case where all the function will be called
#if all(x in func_call for x in ['alignment','adapter_trimming','filtering','plotting']):
if len(func_call)==0:
	if 'specific_output' in commands:
		spec_out={}
		tmp_file=open(commands['specific_output'][0])
		for ele in tmp_file:
			if (re.search('--',ele)):
				ele=re.sub('--','',ele)
				tmp=ele.rstrip().split(' ')
				spec_out[tmp[0]]=tmp[1:]
		tmp_file.close()

	entire_output=os.path.dirname(os.path.realpath(__file__))
	if 'entire_output' in commands:
		entire_output=commands['entire_output'][0]

	#trim_adapter
	if all(x in commands for x in ['core_info_file','seq_data','batch','run','conf']):
		core_info_file=commands['core_info_file'][0]
		seq_data=commands['seq_data'][0]
		job_AT=5
		if 'job_AT' in commands:
			job_AT=int(commands['job_AT'][0])
		command=[seq_data,core_info_file,job_AT,entire_output]
		if ('specific_output' in commands) & ('output_AT_core_info' in spec_out):
			output_AT_core_info=spec_out['output_AT_core_info'][0]
			if not os.path.exists(output_AT_core_info):
				os.makedirs(output_AT_core_info)
			command=[seq_data,core_info_file,job_AT,output_AT_core_info]
		adapter_trimming.concat_func(command)
		#print(command)

		#alignment through gotcloud
		trimmed_file=seq_data
		job_align=3
		if 'job_align' in commands:
			job_align=int(commands['job_align'][0])
		conf=commands['conf'][0]
		batch=commands['batch'][0]
		run=commands['run'][0]
		out_conf=re.sub('(/\w*\w\Z)','',conf)
		if 'specific_output' in commands:
			if 'out_bam' in spec_out:
				out_bam=spec_out['out_bam'][0]
				if not os.path.exists(out_bam):
					os.makedirs(out_bam)
					if not os.path.exists(out_bam+'/Batch'+batch+'_Run'+run):
						os.system('mkdir '+out_bam+'/Batch'+batch+'_Run'+run)
				out_bam=out_bam+'/Batch'+batch+'_Run'+run
		else:
			os.system('mkdir '+entire_output+'/gotcloud_alignment')
			out_bam=entire_output+'/gotcloud_alignment'

		command=[out_bam,trimmed_file,out_conf,job_align,batch,run,conf]
		alignment_gotcloud.concat_func(command)
		#print(command)

		#filter the reads
		in_bam=out_conf+'/metagotCloudbamfiles_Batch'+batch+'_Run'+run
		job_filter=5
		if 'job_filter' in commands:
			job_filter=int(commands['job_filter'][0])

		if 'specific_output' in commands and 'out_proc_bam' in spec_out:
			out_proc_bam=spec_out['out_proc_bam'][0]
			in_bam_filtered=out_proc_bam+'/metagotCloudbamfiles_filtered_Batch'+batch+'_Run'+run
			if not os.path.exists(out_proc_bam):
				os.makedirs(out_proc_bam)
				if not os.path.exists(out_proc_bam+'/Batch'+batch+'_Run'+run):
					os.system('mkdir '+out_proc_bam+'/Batch'+batch+'_Run'+run)
			out_proc_bam=out_proc_bam+'/Batch'+batch+'_Run'+run
		else:
			os.system('mkdir '+entire_output+'/filtering')
			out_proc_bam=entire_output+'/filtering'
			in_bam_filtered=out_proc_bam+'/metagotCloudbamfiles_filtered_Batch'+batch+'_Run'+run

		intermediate_file=False
		if 'intermediate_file' in commands:
			if commands['intermediate_file'][0] in ['Yes']:
				intermediate_file=True
		command=[in_bam,out_proc_bam,job_filter,intermediate_file,batch,run]
		filtering.concat_func(command)
		#print(command)

		#plotting
		if 'specific_output' in commands and 'out_plot' in spec_out:
			out_plot=spec_out['out_plot'][0]
			if not os.path.exists(out_plot):
				os.makedirs(out_plot)
		else:
			os.system('mkdir '+entire_output+'/plot')
			out_plot=entire_output+'/plot'

		os.system('Rscript insertsizehist.R '+in_bam+' '+out_plot+'/metagotCloudbamfiles_Batch'+batch+'_Run'+run+'.pdf')
		os.system('Rscript insertsizehist.R '+in_bam_filtered+' '+out_plot+'/metagotCloudbamfiles_filtered_Batch'+batch+'_Run'+run+'.pdf')

	else:
		print('Please specify at least the --core_info_file --seq_data --batch --run --conf')

elif func_call==['adapter_trimming']:
	if all(x in commands for x in ['core_info_file','seq_data']):
		core_info_file=commands['core_info_file'][0]
		seq_data=commands['seq_data'][0]
		job_AT=5
		if 'job_AT' in commands:
			job_AT=int(commands['job_AT'][0])
		output_AT_core_info=os.path.dirname(os.path.realpath(__file__))
		if 'output_AT_core_info' in commands:
			output_AT_core_info=commands['output_AT_core_info'][0]
		command=[seq_data,core_info_file,job,output_AT_core_info]
		adapter_trimming.concat_func(command)
	else:
		print('Please specify at least the --core_info_file --seq_data')

elif func_call==['alignment']:
	if all(x in commands for x in ['trimmed_file','out_conf','out_bam','batch','run','conf']):
		trimmed_file=commands['trimmed_file'][0]
		job_align=3
		if 'job_align' in commands:
			job_align=int(commands['job_align'][0])
		out_conf=commands['out_conf'][0]
		batch=commands['batch'][0]
		run=commands['run'][0]
		out_bam=commands['out_bam'][0]
		if not os.path.exists(out_bam):
			os.makedirs(out_bam)
			if not os.path.exists(out_bam+'/Batch'+batch+'_Run'+run):
				os.system('mkdir '+out_bam+'/Batch'+batch+'_Run'+run)
		out_bam=out_bam+'/Batch'+batch+'_Run'+run
		command=[out_bam,trimmed_file,out_conf,job_align,batch,run,conf]
		alignment_gotcloud.concat_func(command)
	else:
		print('Please at least specify the pathway to trimmed_file(--trimmed_file),')
		print('pathway to store config files(--out_conf), pathway to store output bam files(--out_bam)')
		print('batch number(--batch) and run number(--run)')

elif func_call==['filtering']:
	if all(x in commands for x in ['out_proc_bam','in_bam']):
		in_bam=commands['in_bam'][0]
		job_filter=5
		if 'job_filter' in commands:
			job_filter=int(commands['job_filter'][0])
		batch=commands['batch'][0]
		run=commands['run'][0]
		out_proc_bam=commands['out_proc_bam'][0]
		if not os.path.exists(out_proc_bam):
			os.makedirs(out_proc_bam)
			if not os.path.exists(out_proc_bam+'/Batch'+batch+'_Run'+run):
				os.system('mkdir '+out_proc_bam+'/Batch'+batch+'_Run'+run)
		out_proc_bam=out_proc_bam+'/Batch'+batch+'_Run'+run
		intermediate_file=False
		if 'intermediate_file' in commands:
			if commands['intermediate_file'][0] in ['Yes','yes','Y','y']:
				intermediate_file=True
		command=[in_bam,out_proc_bam,job_filter,intermediate_file,batch,run]
		filtering.concat_func(command)
	else:
		print('Please at least specify the --in_bam, --out_proc_bam, --batch, --run')

elif func_call==['plotting']:
	if all(x in commands for x in ['in_bam','in_bam_filtered','out_plot']):
		in_bam=commands['in_bam'][0]
		in_bam_filtered=commands['in_bam_filtered'][0]
		out_plot=commands['out_plot'][0]
		batch=re.search('(Batch\d*\d)',in_bam).group(1)
		run=re.search('(Run\d*\d)',in_bam).group(1)
		os.system('Rscript insertsizehist.R '+in_bam+' '+out_plot+'/metagotCloudbamfiles_'+batch+'_'+run+'.pdf')
		os.system('Rscript insertsizehist.R '+in_bam_filtered+' '+out_plot+'/metagotCloudbamfiles_filtered_'+batch+'_'+run+'.pdf')
