import random 
import math
import pdb

GENE_LEN = 10 # need to be bigger than 1

coordinate_list = {1 : [7, 11], 2 : [3, 6], 3 : [1, 5], 4 : [17, 5], 5: [15, 13],
                    6 : [12, 7], 8 : [13, 19], 9 : [7, 9], 10 : [18, 17] }
#generate random initial gene 
#start_point need to be key of dict
def GeneInit(gene_num, start_point):
    gene_arr = [None] * gene_num
    for i in range(0, gene_num):
        gene_arr[i] = [None] * GENE_LEN
        gene_arr[i][0] = start_point
        nucleic_arr = [None] * GENE_LEN
        for j in range(1, GENE_LEN+1):
            nucleic_arr[j-1] = j
        nucleic_arr.pop(start_point-1)
        for j in range(1, GENE_LEN):
            val = random.randrange(0, len(nucleic_arr))
            gene_arr[i][j] = nucleic_arr[val] 
            nucleic_arr.pop(val)

    return gene_arr

def GetDistance(pt1, pt2):
    pdb.set_trace()
    return round( math.sqrt( ( (pt1[0] - pt2[0]) ** 2 ) + ( (pt1[1] - pt2[1]) ** 2 ) ), 3)

def Fitness(gene):
    dist_total = GetDistance(coordinate_list.get(gene[GENE_LEN-1]), coordinate_list.get(gene[0]))
    for i in range(0, GENE_LEN-1):
        dist_total += GetDistance(coordinate_list.get(gene[i]), coordinate_list.get(gene[i+1]))


#print(coordinate_list.get(1)[0])
    
#gene_arr = GeneInit(10,  3)

#gene = gene_arr[0]

#dist = GetDistance(coordinate_list.get(gene[0]), coordinate_list.get(gene[1]))

#print("dist = %f" % dist)
    

gene_arr = GeneInit(10, 3)  
for i in range(10):
    print('[', end = '')
    for j in range(GENE_LEN):
        print(' %d ' % gene_arr[i][j], end ='')
    print(']', end = '')
    print(' |  FITNESS : %f ' % Fitness(gene_arr[i]))
       
print(gene_arr)

print(GetDistance(coordinate_list.get(1), coordinate_list.get(2)))

            
