import subprocess
from spmf import Spmf
import math

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
    results = subprocess.run(['python','main.py', config_file], capture_output=True)
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
    #rspmf = result_spmf( run_spmf("PrefixSpan",'../data/short_d.spmf', "output.spmf",1, 200) )
    # ralg = result_seqalgorithms( run_seqalgorithms("PrefixSpan", '../data/short_d.spmf', "output_short.json", 2, 4, None, 0,"config.cfg" ,-1))
    # print(rspmf, ralg)
    
    ## algorithm = PrefixSpan, GSP
    ## MT.. limit [700 500 200 100] min_support [0.1 0.2 0.3 0.4 0.5]  and up max_length 
    ## input= [ Fifa, kosarak, ]
    
    input_ = "../data/kosarak_sequences.spmf"
    limit_ = [1000,700, 500, 200, 100]
    # min_support_= [0.99, 0.95, 0.90, 0.85]
    
    ## limit_kosarak= [ Max, 500 000, 100 000, 50 000,  10 000, 5000 ]
    ## limit_fifa = [Max, 15 000, 10 000, 5000, 1000, 500]
    ## min_support_fifa= [ 0.15, 0.2, 0.3, 0.4, 0.5]
    min_support_ = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4]
    ## max_length_fifa = [Inf,50, 30, 20 ]
    ## max_lengths_kosarak = [in, 15, 10, 8, 5]
    results_file = 'test.csv'
    algorithm_ = "GSP"
    input_ = "../data/kosarak_sequences.spmf"
    # limit_ = [None,15000, 10000, 5000, 1000, 500]
    min_support_ = [  0.35, 0.36, 0.45,0.3, 0.4, 0.5, 0.6]
    #min_support_ = [0.35, 0.36, 0.45]
    # max_length_ = [None,50, 30, 20]
    
    # input_="../data/kosarak_sequences.spmf"
    # limit_ = [None, 500000, 100000, 50000,  10000, 5000]
    # min_support_= [ 0.1, 0.15, 0.2, 0.3, 0.4]
    # max_length_ = [None, 15, 10, 8, 5]
    limit_ = [None]
    #min_support_ = [0.35]
    max_length_ = [False]
    #min_support_ = [0.99]
    #with open(results_file, 'a') as f:
    #    f.write('algorithm, program,input_file, output_file, min_support, max_length, min_length, limit, time, freq_seq\n')
        
    # ralg = result_seqalgorithms( run_seqalgorithms("PrefixSpan", '../data/short_d.spmf', "output_short.json", 2, 4, None, 0,"config.cfg" ,-1))
    # print( ralg)
    i = 1
    # output_ = "output_"+algorithm_+"_fifa_"+str(i)+".json"
    # ralg = result_seqalgorithms( run_seqalgorithms(algorithm_,input_, output_,min_support_[0] , max_length_[0], limit_[0], 0,"config.cfg" ,-1))
    # min_ = min_support_[0]
    # max_ = max_length_[0]
    # lim_ = limit_[0]
  
    ##algorithm, input_path, output_path, min_support, max_length, limit, min_length, config_file, splitte
    for min_ in min_support_:
        for max_ in max_length_:
            for lim_ in limit_:
                output_ = "spmf_output_"+algorithm_+"_covid_"+str(i)+".json"
                rspmf = result_spmf( run_spmf(algorithm_,input_, "output.spmf",min_,max_) )
               # ralg =  result_seqalgorithms( run_seqalgorithms(algorithm_,input_, output_,min_ , max_, lim_, 0,"config.cfg" ,-1))
                print(rspmf)
                with open(results_file, 'a') as f:
                    f.write(algorithm_+", spmf ,"+input_+","+ output_+","+str(min_)+","+str(max_)+",0,"+str(lim_)+", {},{}\n".format(rspmf['time'], rspmf['found_seq']))
               # with open(results_file, 'a') as f:
                #    f.write("GSP, seqalgorithms ,"+input_+","+ output_+","+str(min_)+","+str(max_)+",0,"+str(lim_)+", {},{}\n".format(ralg['time'], ralg['found_seq']))
                i+=1
        
    print(min_support_[0], max_, lim_)
        #ralg = result_seqalgorithms( run_seqalgorithms(algorithm_,input_, output_,min_support_[0] , max_length_[0], limit_[0], 0,"config.cfg" ,-1))
        #print(i,ralg)
        