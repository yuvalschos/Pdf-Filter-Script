# Pdf-Filter-Script

Python Script that scans source folder with pdf files and moves them to target folder according to filter parameters.

The script scans every pdf file and searches for keywords and dates.

Important to know!
 - dates range: if one date in the range is in your pdf it will be considered as found.
 - must have keywords: all of the words must appear in the file to be considered as found.
 - if the two conditions exist then the file move to the target filter.
 - dates format: dd/mm/yyyy for example 20/11/2022
 - keywords format: word1,word2,word3,... (no spaces or any other signs)
