# Parsers Library
this section contains custom built parsers for different data sets that dont fit the standard syslog specs. they are nested in a similar structure to the rest of this repo.

## How to use
any parser you want to use needs to be appended to the default parser set and named parsers.conf 
1. Copy the desired config from the conf file in this repo
2. Append to the end of the default parsers.conf file
3. Delete the old parsers.conf file from your pipeline and replace with your updated file
4. Validate parsing with standard output

if you need the default parsers file, or want to better understand parser configs check [the fluentbit docs on parsers.](https://docs.fluentbit.io/manual/pipeline/parsers/configuring-parser)