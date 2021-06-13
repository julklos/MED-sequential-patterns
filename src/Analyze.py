import subprocess
from spmf import Spmf

def create_config(confname, algorithm, limit, input, output, min_support, max_length, min_length, splitter):

    config = (
        "[configuration]\n"
        "algorithm = {algorithm}\n"
        "limit = {limit}\n"
        "input = {input}\n"
        "output = {output}\n" 
        "min_support = {min_support}\n"
        "max_length = {max_length}\n"
        "min_length = {min_length}\n"
        "splitter = {splitter}\n"
    )

    config = config.format(
        algorithm = algorithm,
        limit = limit,
        input = input,
        output = output,
        min_support = min_support,
        max_length = max_length,
        min_length = min_length,
        splitter = splitter
    )

    with open(confname, 'w') as f:
        f.write(config)

def run_spmf(algorithm, input_path, output_path, min_support, max_length):

    spmf = Spmf(algorithm, input_filename=input_path, output_filename=output_path, 
                        spmf_bin_location_dir="../env/Lib/site-packages/spmf/", arguments=[min_support, max_length])
    
    results =  spmf.run()
    return results

def result_spmf(output):
    lines = output.split('\n')
    results = {}

    for l in lines:
        if "Total time" in l:
            res = [i for i in l.split(' ')]
            results['time'] = res[4]
        elif "Frequent sequences count" in l:
            res = [i for i in l.split(' ')]
            results['found_seq'] = res[5]
    
    return results
    

def run_seqalgorithms(algorithm, input_path, output_path, min_support, max_length, limit, min_length, config_file, splitter):
    create_config(config_file, algorithm, limit, input_path, output_path, min_support, max_length, min_length, splitter)
    results = subprocess.run(['python','src/main.py', config_file], capture_output=True)

    return results.stdout

def result_seqalgorithms(output):
    text = output.decode('utf-8')
    lines =  text.split('\n')
    results = {}

    for l in lines:
        if "Time" in l:
            res = [i for i in l.split(' ')]
            results['time'] = res[1]
        elif "Found sequences:" in l:
            res = [i for i in l.split(' ')]
            results['found_seq'] = res[2]
    return results


def compare_output_files(seqalg_out, spmf_out):
    spmf_lines = []
    with open(spmf_out, 'r') as f:
        for _, l in enumerate(f):
            spmf_lines.append(l.split('-1')[0].strip())
    spmf_lines.sort()

    sa_lines = []
    #TODO: read JSON
    # with open(seqalg_out, 'r') as f:
    #     for _, l in enumerate(f):
    #         sa_lines.append(l.strip())

    return set(spmf_lines) == set(sm_lines)

if __name__ == "__main__":

    #TO DO: MOZNA STWORZYC PETLE DLA JAKICH PARAMETROW
    rspmf = result_spmf( run_spmf("PrefixSpan",'../data/short_d.spmf', "output.spmf",2, 200) )
    ralg = result_seqalgorithms( run_seqalgorithms("PrefixSpan", 'data/short_d.spmf', "output_short.json", 2, 4, None, 0,"config.cfg" ,-1))
    print(rspmf, ralg)
    results_file = 'test.csv'
    with open(results_file, 'a') as f:
        f.write('algorithm, program,input_file, output_file, min_support, max_length, min_length, limit, time, freq_seq\n')

    with open(results_file, 'a') as f:
        f.write('PrefixSpan, seqalgorithms ,data/short_d.spmf, output_short.json, 2, 4, 0, None, {},{}\n'.format(ralg['time'], ralg['found_seq']))