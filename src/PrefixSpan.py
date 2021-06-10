from SequentialPatternAlgorithm import SequentialPatternAlgorithm

class PrefixSpan(SequentialPatternAlgorithm):

    PLACEHOLDER = "_"

    def run(self):

        self._prefix_span([], self._data)
        return self._data

    def _prefix_span(self, alpha, sequencesDb):
        freq = self._frequency_items(alpha, sequencesDb)
        print(freq)

        # for every pattern p in freq
        # p can be assembled to the last element of alpha or can be add as sequential pattern
        for f in freq :    
            newAlpha = []

            # if _item
            if "_" in f :
                for itemset in alpha :
                    newAlpha.append(itemset)

                #get the last element of alpha    
                newItemset = newAlpha[-1]
                f.remove('_')
                newItemset.append(f)
                newItemset.sort()
                # assemble p as the last element of alpha
                newAlpha[-1] = newItemset

            # if item
            else :
                if len(alpha) != 0:
                    for itemset in alpha :
                        newAlpha.append(itemset)
                
                newItemset = [f]
                newAlpha.append(newItemset)

            print(newAlpha)


    def _getSuffix(self, sequence, prefix):
        found = False

        for i,itemset in enumerate(sequence):
            if self._containAll(prefix,itemset):
                found = True
                break

            else :
                item_tmp = itemset[0].copy()
                if len(prefix) > 0 and '_' in itemset[0] and prefix[-1] == item_tmp.remove('_'):
                    found = True
                    break

        if found:
            suffix = sequence[i:].copy()
            first_suffix = suffix[0]

            if '_' in first_suffix[0] :
                    first_suffix.pop(0)
            else :
                to_delete = []
                itemset_new = self._removeAll(first_suffix, prefix)
                for item in enumerate(itemset_new):
                    if item < prefix[-1]:
                        to_delete.append(item)
                for e in to_delete:
                     itemset_new.remove(item)

            if len(itemset_new) != 0 :
                itemset_new.sort()
                suffix[0] = itemset_new
            else : suffix.pop[0]

            return suffix
            
        else: return None


    def _frequency_items(self, alpha, sequencesDb):

        seqFreq = {}

        #get the last itemset of alpha
        if len(alpha) != 0:
            last_itemset = alpha[-1]
        else:
            last_itemset = []

        for sequence in sequencesDb :

            for itemset in sequence.get_itemsets():
                #see if the itemset contains all items from alpha last itemset
                #if yes then item after the last item of alpha last itemset as _item and item
                if len(last_itemset) != 0 and self._containAll(itemset, last_itemset):
                    
                    # add item in last itemset in alpha
                    for item in last_itemset:
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1
                    
                    # add items not included in alpha last itemset
                    leftItemset = self._removeAll(itemset.copy(), last_itemset)
                    for item in leftItemset :
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1

                        if "_" + item in seqFreq:
                            seqFreq["_" + item] = seqFreq[item] +1
                        else:
                            seqFreq["_" + item] = 1
                    
                else:
                    for item in itemset:
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1

        #remove infrequent items
        newSeqFreq = dict((k,v) for k,v in seqFreq.items() if v > self._min_support)
        return newSeqFreq



    def _containAll(self, list1, list2):

        ifContains = True
        for item in list1:
            if item not in list2:
                ifContains = False
                break
        
        return ifContains

    def _removeAll(self, list1, list2):

        for item in list1:
            if item in list2:
                list1.remove(item)

        return list1