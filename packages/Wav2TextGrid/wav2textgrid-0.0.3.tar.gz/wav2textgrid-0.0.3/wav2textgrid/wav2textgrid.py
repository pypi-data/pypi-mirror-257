#!/usr/bin/env python3
import glob
import os
import pickle as pkl
import torch
from aligner_core.xvec_extractor import xVecExtractor
from aligner_core.aligner import xVecSAT_forced_aligner
import argparse

def align_file(args):
    xvx = xVecExtractor(method='xvector')

    xvector = xvx.extract_xvector(args.wavfile_or_dir)
    xvector = xvector[0][0].view(1, -1)
    if torch.cuda.is_available():
        xvector = xvector.cuda()

    aligner = xVecSAT_forced_aligner('pkadambi/Wav2TextGrid', satvector_size=512)
    transcript = open(args.transcriptfile_or_dir, 'r').readlines()[0]
    transcript = transcript.replace('\n', '')
    aligner.serve(audio=args.wavfile_or_dir, text=transcript, save_to=args.outfile_or_dir, ixvector=xvector)


def align():
    parser = argparse.ArgumentParser()
    parser.add_argument('wavfile_or_dir', type=str)
    parser.add_argument('transcriptfile_or_dir', type=str)
    parser.add_argument('outfile_or_dir', default=str)
    args = parser.parse_args()

    if os.path.isdir(args.wavfile_or_dir):
        align_dirs(args)
    else:
        align_file(args)


def align_dirs(args):
    # Get list of .wav files in directory1 and its subdirectories
    wav_files = glob.glob(os.path.join(args.wavfile_or_dir, '**/*.wav'), recursive=True)
    # Get list of .lab files in directory2 and its subdirectories
    lab_files = glob.glob(os.path.join(args.transcriptfile_or_dir, '**/*.lab'), recursive=True)
    success_count = 0
    failure_count = 0
    missing_lab_files = []
    # Iterate over .wav files
    for wav_file in wav_files:
        # Generate corresponding .lab file path
        rel_path = os.path.relpath(wav_file, args.wavfile_or_dir)
        lab_file = os.path.join(args.transcriptfile_or_dir, os.path.splitext(rel_path)[0] + '.lab')

        # Check if .lab file exists
        if os.path.exists(lab_file):
            try:
                # Align .wav and .lab files
                align(wav_file, lab_file)
                success_count += 1
            except Exception as e:
                print(f"Alignment failed for {wav_file}: {e}")
                failure_count += 1
        else:
            missing_lab_files.append(lab_file)
            print(f"Did not find transcript at {lab_file} for wav file {wav_file}")

        # Write to alignment log
    with open(os.path.join(args.output_directory_or_filepath, 'alignment.log'), 'w') as log_file:
        log_file.write(f"Successfully aligned: {success_count}\n")
        log_file.write(f"Alignment failures: {failure_count}\n")
        if missing_lab_files:
            log_file.write("\nMissing transcript files:\n")
            for missing_lab_file in missing_lab_files:
                log_file.write(f"- {missing_lab_file}\n")

    pass


if __name__=='__main__':
    align()
    # xvx = xVecExtractor(method='xvector')
    #
    # xvector = xvx.extract_xvector('./examples/test.wav')
    #
    # aligner = xVecSAT_forced_aligner('./wav2textgrid_model', satvector_size=150)
    # transcript = open('./examples/test.lab', 'r').readlines()[0]
    # transcript = transcript.replace('\n', '')
    # xvector = xvector[0][0].view(1, -1)
    #
    # if CUDA_AVAILABLE:
    #     xvector = xvector.cuda()
    #
    # # aligner.serve(audio='./examples/test.wav', text=transcript, save_to='./examples/test.TextGrid', ixvector=xvector)
    # aligner.serve(audio='./examples/test.wav', text=transcript, save_to='./examples/test.TextGrid', ixvector=xvector)