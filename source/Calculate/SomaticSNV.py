import os,re
import sys
import optparse
import time

HelpInfo = 'python SomaticSNV.py -i <single-cell.vcf> -g <Germline.vcf> -o <output.vcf>'
parser=optparse.OptionParser(HelpInfo)
parser.add_option('-i', '--input', dest='scSNV',type=str, help='single-cell vcf')
parser.add_option('-g', '--germline', dest='Germline', type=str, help='Germline vcf')
parser.add_option('-o', '--output', dest='outfile', type=str, help='output vcf')
options, args = parser.parse_args()
def ParseVCF(aimvcf):
    # input a vcf file get the SNV positions and information into dict
    SNV_dict = {}
    header = ''
    with open(aimvcf) as f:
        for records in f.readlines():
            if not re.search('#', records):
                # the information part
                Info = records.strip().split("\t")
                Pos = Info[0] + ":" + Info[1] +"_" + Info[3] + "_" + Info[4]
                SNV_dict[Pos] = records
            else:
                header += records

    return(SNV_dict, header)


scdict, scHeader = ParseVCF(options.scSNV)
print('%s: Load %s SNVs from single-cell sample' % (time.ctime(), len(scdict.keys())))
gmdict, gmHeader = ParseVCF(options.Germline)
print('%s: Load %s SNVs from germline sample' % (time.ctime(), len(gmdict.keys())))
somatic_keys = scdict.keys() - gmdict.keys()
with open(options.outfile, 'w') as output:
    output.write(scHeader)
    output.flush()
    for k in somatic_keys:
        output.write(scdict[k])
        output.flush()
    print('%s: The somatic mutation has been written in file: %s' % (time.ctime(), options.outfile))
