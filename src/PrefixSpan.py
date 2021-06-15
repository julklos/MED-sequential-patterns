from SequentialPatternAlgorithm import SequentialPatternAlgorithm
from Sequence import Sequence
from ClientSequence import ClientSequence
from timeit import default_timer as timer
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class PrefixSpan(SequentialPatternAlgorithm):

    PLACEHOLDER = "_"

    def run(self):

        logging.info("Algorithm parameters:")
        logging.info("Min support: " +str(self._min_support))
        logging.info("Max length pattern: " + str(self._max_seq_length))
        logging.info("Min length pattern: " + str(self._min_seq_length))
        logging.info("Rows: " + str(len(self._data)))
        logging.info("Start Prefix Span Algorithm...")
        self._final_sequences = []
        start = timer()
        self._prefix_span(ClientSequence([]), self._data)
        stop = timer()
        self._time = (stop - start)
        logging.info("Stop Prefix Span Algorithm...")
        logging.info("Time:" + str(self._time ))
        output = self._createOutputDicrionary()
        return output

        #TODO clear final_sequences

    def _prefix_span(self, alpha, sequencesDb):
        """
        Recursive function for PrefixSpan algorithm
        :param alpha: sequential pattern
        :param sequencesDb: projected database for alpha
        """

        freq = self._frequency_items(alpha, sequencesDb)                                                
        if len(alpha.get_pattern()) >= self._max_seq_length:                                                    
            return 
        
        for f in freq :                                                                                           
            newAlpha = []

            #f can be assembled to the last element of alpha(pattern)
            if self.PLACEHOLDER in f :
                for itemset in alpha.get_pattern() :
                    newAlpha.append(itemset)
 
                newItemset = newAlpha[-1].copy()
                newItemset.append(f[1:])
                newItemset.sort()
                newAlpha[-1] = newItemset

            #or can be added as sequential pattern
            else :
                if len(alpha.get_pattern()) != 0:
                    for itemset in alpha.get_pattern() :
                        newAlpha.append(itemset)
                
                newItemset = [f]
                newAlpha.append(newItemset)

            if alpha.get_value() < 0 :
                newAlphafreq = freq[f]
            else :
                newAlphafreq = min(freq[f], alpha.get_value())

            #create new pattern    
            newPattern = ClientSequence(newAlpha, newAlphafreq)
            if newPattern.get_pattern_size() >= self._min_seq_length:
                self._final_sequences.append(newPattern)

            #build projected database
            projectedDb = []
            for sequence in sequencesDb :
                suffix = self._getSuffix(sequence, newPattern.get_pattern()[-1])
                if suffix != None and len(suffix.get_itemsets()) != 0 :
                    projectedDb.append(suffix)
            
            if len(projectedDb) != 0 :
                self._prefix_span(newPattern, projectedDb)
               

    def _getSuffix(self, sequence, prefix):
        """
        Return suffix for a given sequence and prefix
        """

        #find first itemset that can be part of suffix 
        found = False
        if len(sequence.get_itemsets()) == 0 :
            return    
        for i,itemset in enumerate(sequence.get_itemsets()):
            if self._containAll(itemset,prefix):
                found = True
                break

            else :
                if len(prefix) > 1 and self.PLACEHOLDER in itemset and prefix[-1] in itemset[0]:
                    found = True
                    break

        if found:
            index = itemset.index(prefix[-1])

            #if the last element of prefix is the last element in itemset
            if index == len(itemset) - 1:
                suffix = sequence.get_itemsets()[i+1:]
            else:
                suffix = sequence.get_itemsets()[i:]
                e = itemset[index:]
                e[0] = self.PLACEHOLDER
                suffix[0] = e

            if len(suffix) > 0 :
                return Sequence(suffix)
            else: return None
            
        else: return None


    def _frequency_items(self, alpha, sequencesDb):
        """
        Return frequent elements
        :param alpha: sequential pattern
        """

        seqFreq = {}
        _seqFreq = {}

        if len(alpha.get_pattern()) != 0:
            last_itemset = alpha.get_pattern()[-1]
        else:
            last_itemset = []
    
        for sequence in sequencesDb :
                flag_ignore = False

                #first itemset contains last_itemset of alpha and last element of last_itemset is not the last element in first itemset
                if len(last_itemset) != 0 and self._containAll(sequence.get_itemsets()[0], last_itemset):
                    index = sequence.get_itemsets()[0].index(last_itemset[-1])
                    if index < len(sequence.get_itemsets()[0]) - 1:
                        for item in sequence.get_itemsets()[0][index + 1]:
                            if item in _seqFreq:
                                _seqFreq[item] += 1
                            else:
                                _seqFreq[item] = 1
                    
                #first itemset begin with place holder
                if self.PLACEHOLDER in sequence.get_itemsets()[0]:
                    for item in sequence.get_itemsets()[0][1:]:
                        if item in _seqFreq:
                            _seqFreq[item] += 1
                        else:
                            _seqFreq[item] = 1
                    flag_ignore = True
    
                counted = []
                for itemset in sequence.get_itemsets() :
                    if flag_ignore:
                        flag_ignore = False
                        continue
                    for item in itemset:
                        if item not in counted and item != self.PLACEHOLDER:
                            counted.append(item)
                            if item in seqFreq:
                                seqFreq[item] += 1
                            else:
                                seqFreq[item] = 1
                


        #remove infrequent items
        newSeqFreq = {}
        for k,v in seqFreq.items() :
            if v >= self._min_support :
                newSeqFreq[k] = v
        for k,v in _seqFreq.items() :
            if v >= self._min_support :
                newSeqFreq[self.PLACEHOLDER + k] = v
        
        return newSeqFreq

    def _containAll(self, list1, list2):

        ifContains = True
        for item in list2:
            if item not in list1:
                ifContains = False
                break
        
        return ifContains

    
    def _createOutputDicrionary(self):
        output = {}
        parameters = {}
        sequences = {}

        parameters['algorithm'] = 'PrefixSpan'
        parameters['min_support'] = self._min_support_frac
        parameters['max_seq_length'] = self._max_seq_length
        parameters['min_seq_length'] = self._min_seq_length

        for i,seq in enumerate(self._final_sequences) :
            s = {}
            s['pattern'] = seq.get_pattern()
            s['support'] = seq.get_value()
            sequences[i] = s

        output['parameters'] = parameters
        output['rows'] = len(self._data)
        output['found_seq'] = len(self._final_sequences)
        output['time'] = self._time
        output['sequences'] = sequences
    
        return output