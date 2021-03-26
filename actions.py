# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, ActionExecutionRejection, Tracker
from rasa_sdk.events import (ActionExecuted, ActionReverted, Restarted,
                                  SlotSet, UserUtteranceReverted, UserUttered)
from rasa_sdk.executor import CollectingDispatcher

# selenium kütüphaneleri
from selenium import webdriver #Bir tarayıcıyı başlatmanıza / başlatmanıza izin verir
from selenium.webdriver.common.keys import Keys # 
from selenium.webdriver.common.by import By  #Belirli parametreleri kullanarak şeyler aramanıza izin verir
from selenium.webdriver.support.ui import WebDriverWait # açılan tarayıcada kalmamızı sağlar
from selenium.webdriver.support import expected_conditions as EC # belirli bir koşulun oluşmasını beklemek için tanımlanan bir koddur
from selenium.webdriver.chrome.options import Options # Tarayıcı ayarlarını yapmak için kullanılır

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_kelime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kelime = tracker.get_slot("kelime")
        
        
        kelime = str(kelime)
        #%%
        driver_path = "chromedriver.exe"
        ayarlar = Options()
        ayarlar.add_argument("--headless")  #tarayıcıyı açmadan veri çekmeyi sağlar 
        browser = webdriver.Chrome(executable_path=driver_path,options=ayarlar)     
        browser.get('https://sozluk.gov.tr/')
        arama = browser.find_element_by_name('q')
        arama.send_keys(kelime)
        arama.send_keys(Keys.RETURN)
        try:
            main = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.ID, "anlamlar-gts0")))
            # print(main.text)
            anlam =("{}".format(main.text))
            print(anlam)
        except:
            message = ("{} adlı kelime bulunamadı".format(kelime))
            browser.quit()
            #%%        


         
        message = "{}: {}".format(kelime,anlam)
        
        print(message)
        
        dispatcher.utter_message(text=message)

        return [(SlotSet("kelime",kelime)),message]
