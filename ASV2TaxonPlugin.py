import sys
import numpy



class ASV2TaxonPlugin:
   def input(self, filename):
      self.myfile = filename

   def run(self):
      filestuff = open(self.myfile, 'r')
      self.firstline = filestuff.readline().strip()
      classification = self.firstline.split(',')
      #lines = []
      self.taxa = dict()
      self.counts = dict()
      for myline in filestuff:
         line = myline.strip()
         contents = line.split(',')
         asv = contents[0]
         i = 1
         previous = ""
         current = ""
         while (i < len(contents) and contents[i] != "NA"):
            previous = current
            current = contents[i]
            i += 1
         if (i == 8):  # Species-level, include both
            taxon = previous+"_"+current
         elif (i == 7): # Genus level, just use itself
            taxon = current
         elif (i == 1): # Not classifiable at all
            taxon = "Unclassified"
         else:  # Above genus level, attach classification
            taxon = current+"("+classification[i-1]+")"
         if taxon not in self.counts:
            self.counts[taxon] = 0
         else:
            self.counts[taxon] += 1
            taxon = taxon + "-" + str(self.counts[taxon])
         # Remove any inner quotes
         taxon = taxon.replace('\"','')
         taxon = "\"" + taxon + "\""
         self.taxa[asv] = taxon

   def output(self, filename):
      filestuff2 = open(filename, 'w')
      
      filestuff2.write("\"\",\"Taxon\"\n")
      for asv in self.taxa:
         filestuff2.write(asv+","+self.taxa[asv]+"\n")



