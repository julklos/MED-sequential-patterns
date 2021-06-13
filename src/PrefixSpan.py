from SequentialPatternAlgorithm import SequentialPatternAlgorithm
from Sequence import Sequence
from ClientSequence import ClientSequence
from timeit import default_timer as timer

class PrefixSpanAlgorithm(SequentialPatternAlgorithm):

    PLACEHOLDER = "_"

    def run(self):
        print("Start Prefix Span Algorithm...")
        print("Min support:" +str(self._min_support))
        print("Sequences: " + str(len(self._data)))
        self._final_sequences = []
        start = timer()
        self._prefix_span(ClientSequence([]), self._data)
        stop = timer()
        self._time = (stop - start)
        print("Stop Prefix Span Algorithm...")
        output = self._createOutputDicrionary()
        return output

#TODO clear final_sequences

    def _prefix_span(self, alpha, sequencesDb):

        freq = self._frequency_items(alpha, sequencesDb)
        if len(alpha.get_pattern()) >= self._max_seq_length:
            return 
        # for every pattern p in freq
        # p can be assembled to the last element of alpha or can be add as sequential pattern
        for f in freq :  
            newAlpha = []

            # if _item
            if "_" in f :
                for itemset in alpha.get_pattern() :
                    newAlpha.append(itemset)

                #get the last element of alpha    
                newItemset = newAlpha[-1].copy()
                newItemset.append(f[1:])
                newItemset.sort()
                # assemble p as the last element of alpha
                newAlpha[-1] = newItemset

            # if item
            else :
                if len(alpha.get_pattern()) != 0:
                    for itemset in alpha.get_pattern() :
                        newAlpha.append(itemset)
                
                newItemset = [f]
                newAlpha.append(newItemset)
            #TO DO: find the suuport of Patern and take min - class Pattern
            if alpha.get_value() < 0 :
                newAlphafreq = freq[f]
            else :
                newAlphafreq = min(freq[f], alpha.get_value())
            newPattern = ClientSequence(newAlpha, newAlphafreq)
            if newPattern.get_pattern_size() >= self._min_seq_length:
                self._final_sequences.append(newPattern)

            projectedDb = []

            for sequence in sequencesDb :
                suffix = self._getSuffix(sequence, newPattern.get_pattern()[-1])
                if suffix != None and len(suffix.get_itemsets()) != 0 :
                    projectedDb.append(suffix)
            
            if len(projectedDb) != 0 :
                self._prefix_span(newPattern, projectedDb)

    def _removeInfrequentElements(self, sequence, freq):

        projectedSequence = sequence.frequent_item_from_itemset(freq)
        return Sequence(projectedSequence)
                

    def _getSuffix(self, sequence, prefix):
        found = False
        if len(sequence.get_itemsets()) == 0 :
            return    
        for i,itemset in enumerate(sequence.get_itemsets()):
            if self._containAll(itemset,prefix):
                found = True
                break

            else :
                #item_tmp = itemset[0].replace('_', '')
                if len(prefix) > 1 and '_' in itemset and prefix[-1] in itemset[0]:
                    #itemset[0] = itemset[0].replace("_", "")
                    found = True
                    break

        if found:
            # suffix = sequence.get_itemsets()[i:].copy()
            # first_suffix = suffix[0].copy()

            # if '_' in first_suffix[0] :
            #     first_suffix[0] = first_suffix[0].replace("_","")
            # else :
            #     to_delete = []
            #     first_suffix= self._removeAll(first_suffix, prefix)
            #     for item in first_suffix:
            #         if item < prefix[-1]:
            #             to_delete.append(item)
            #     for e in to_delete:
            #          first_suffix.remove(e)

            # if len(first_suffix) != 0 :
            #     first_suffix.sort()
            #     suffix[0] = first_suffix
            # else : 
            #     suffix.pop(0)
            
            # return Sequence(suffix)

            index = itemset.index(prefix[-1])
            if index == len(itemset) - 1:
                suffix = sequence.get_itemsets()[i+1:]
            else:
                suffix = sequence.get_itemsets()[i:]
                e = itemset[index:]
                e[0] = '_'
                suffix[0] = e

            if len(suffix) > 0 :
                return Sequence(suffix)
            else: return None
            
        else: return None


    def _frequency_items(self, alpha, sequencesDb):

        seqFreq = {}
        _seqFreq = {}

        #get the last itemset of alpha
        if len(alpha.get_pattern()) != 0:
            last_itemset = alpha.get_pattern()[-1]
        else:
            last_itemset = []

        # for sequence in sequencesDb :
        #     sequenceItems = set()
        #     for itemset in sequence.get_itemsets():
        #         #see if the itemset contains all items from alpha last itemset
        #         #if yes then item after the last item of alpha last itemset as _item and item
        #         if len(last_itemset) != 0 and self._containAll(itemset, last_itemset):
        #             print(last_itemset)
        #             # add item in last itemset in alpha
        #             for item in last_itemset:
        #                 sequenceItems.add(item)
                    
        #             # add items not included in alpha last itemset
        #             leftItemset = self._removeAll(itemset.copy(), last_itemset)
        #             for item in leftItemset :
        #                 sequenceItems.add(item)
        #                 sequenceItems.add("_" + item)
                    
        #         else:
        #             for item in itemset:
        #                 sequenceItems.add(item)

        # #add sequenceItems to seqFreq
        #     for item in sequenceItems :
        #         if item in seqFreq :
        #             seqFreq[item] = seqFreq[item] + 1
        #         else :
        #             seqFreq[item] = 1

        
        for sequence in sequencesDb :
                flag_ignore = False
                if len(last_itemset) != 0 and self._containAll(sequence.get_itemsets()[0], last_itemset):
                    index = sequence.get_itemsets()[0].index(last_itemset[-1])
                    if index < len(sequence.get_itemsets()[0]) - 1:
                        for item in sequence.get_itemsets()[0][index + 1]:
                            if item in _seqFreq:
                                _seqFreq[item] += 1
                            else:
                                _seqFreq[item] = 1
                    

                if '_' in sequence.get_itemsets()[0]:
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
                        if item not in counted and item != '_':
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
                newSeqFreq['_' + k] = v
        #newSeqFreq = dict((k,v) for k,v in seqFreq.items() if v >= self._min_support)
        
        return newSeqFreq

    def _containAll(self, list1, list2):

        ifContains = True
        for item in list2:
            item2 = item.replace('_', '')
            if item not in list1:
                item2 = item.replace('_', '')
                if item2 not in list1:
                    ifContains = False
                    break
        
        return ifContains

    def _removeAll(self, list1, list2):

        for item in list1:
            if item in list2:
                list1.remove(item)

        return list1
    
    def _createOutputDicrionary(self):
        output = {}
        parameters = {}
        sequences = {}

        parameters['algorithm'] = 'PrefixSpan'
        parameters['min_support'] = self._min_support
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

        print(output)
    
        return output