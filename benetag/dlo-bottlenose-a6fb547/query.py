import bottlenose

amazon = bottlenose.Amazon("AKIAIT4OSXQMYQB2XLUQ", "RPzfxhl7eEa/NiIcmkNinQ8OG6kTW65M6UrRqFgD")
response = amazon.ItemLookup(ItemId="0596520999", ResponseGroup="Images",
SearchIndex="Books", IdType="ISBN",
Style="http://xml2json-xslt.googlecode.com/svn/trunk/xml2json.xslt")
