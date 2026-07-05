from bs4 import BeautifulSoup 
from app.utils.logger import logger 

IGNORED_TAGS = {

    "script",

    "style",

    "footer",

    "header",

    "noscript"
}

IMPORTANT_TAGS = {

    "button",

    "input",

    "textarea",

    "select",

    "label",

    "form",

    "a"
}
class ContextCompressor :
    
    def clean_dom(self,soup):
        logger.info("Cleaning DOM...")
        for tag in soup.find_all(IGNORED_TAGS):
            tag.decompose() 
        
        return soup 
    
    def remove_empty(self,soup):

        for tag in soup.find_all():
            if not tag.get_text(strip=True):
                if not tag.find():
                    tag.decompose() 

        
        return soup 
    
    def extract_ui(self,soup):
        ui= []

        for tag in soup.find_all(IMPORTANT_TAGS):

            ui.append(
                {
                     "tag": tag.name,

                     "text": tag.get_text(strip=True),

                     "id": tag.get("id"),
                     
                     "name": tag.get("name"),
                     
                     "placeholder": tag.get("placeholder"),
                    
                     "type": tag.get("type")

                }
            )
        return ui
    
    def compress(self,extracted):

        soup = extracted["html"]
        ax = extracted["accessibility"]

        soup = self.clean_dom(soup)
        soup = self.remove_empty(soup)

        ui = self.extract_ui(soup)

        return{

            "ui" : ui,
            "accessibility" : ax
        }