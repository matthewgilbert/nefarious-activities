
class ReviewParser(object):
    """
    This class implements a way to seperate a review document into atomic sentences. (defined carefully
     by the periods.)
    methods:
        parse( review ): accepts a string as a review document, and returns a list of the atomic 
                        sentences.
    
    """
    def __init__(self):
        pass
    
    def remove_doublebs( self, review ):
        #remove double backslashes, i.e. redundant escape chars.
        return re.sub( r'\\n', '\n', review )
    
    def handle_currency(self, review):
        """So we need to handle things like '$5.50', to do this I use a placeholder 
        for '.', and then put it back later"""
        safe_replacement = "&&"
        def keep_price(matchobj):
            return matchobj.group(1) + "&&" + matchobj.group(2)
            
        return re.sub( "([0-9]*)\.([0-9]{1,2})", keep_price, review )
    
    def redo_currency(self, sentence ):
        #put the currency back in
        return re.sub( "&&", ".", sentence)
    
    
    def replace_extended_periods( self, review):
        """People like to use .+ often."""
        #this matches '.' and then an positive number of futher periods -- 
        #this means '.' won't be matched, but '..' will.
        review = re.sub( "\.\.+", "--", review ) 
        return review
    
    
    def split_on_paragraphs( self, review ):
        return re.split("\n+", review.strip() )
        
    
    def remove_trailing_space( self, paragraph ):
        #if the do something silly like don't end with a period, things are not good. 
        # this matches any eol, plus whitespace
        def keep_eol( matchobj ):
            if re.findall( '[.!?]', matchobj.group(0) ):
                return matchobj.group(0)
            else:
                return "."
         

        paragraph =  re.sub( "([.!?]*)\s*$", keep_eol, paragraph) 
        return paragraph
    
    
    def split_to_sentences( self, paragraph ):
        # split a paragraph, very carefully, into sentences.
        #we can drop the last because we know it is '', as we have purposefully made sure the end is [?!.]
        it = re.split( '(?!\()([?.!]*)(?!\))', paragraph )[:-1] 
        
        cleaned_text = map(string.strip, it[::2] ) #strings like " I think I like it here" become "I Think I like it here"
        return map( lambda x: x[0]+x[1], zip( cleaned_text, it[1::2] ) ) #"adds the punctuation back in"
   
    def parse(self, review ):
        """
        This is the main method of the class. Call this on a 
        string representing the review and receive a list of the 
        atomic sentences.
        """
        review = self.remove_doublebs( review )
        review = self.replace_extended_periods( review )
        review = self.handle_currency( review )
        paragraphs = self.split_on_paragraphs( review )
        paragraphs = map( self.remove_trailing_space, paragraphs )
        sentences = reduce( lambda x,y: x+y, map( self.split_to_sentences, paragraphs) )
        sentences = map( self.redo_currency, sentences )
        return sentences
        