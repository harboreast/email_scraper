# email_scraper

User-agent: *
Disallow: 

                    _..._
                 .-'     '-.
                /     _    _\
               /':.  (o)  /__)
              /':. .,_    |  |
             |': ; /  \   /_/
             /  ;  `"`"    }
            ; ':.,         {
           /      ;        }
          ; '::.   ;\/\ /\ {
         |.      ':. ;``"``\
        / '::'::'    /      ;
       |':::' '::'  /       |
       \   '::' _.-`;       ;
       /`-..--;` ;  |       |
      ;  ;  ;  ;  ; |       |
      ; ;  ;  ; ;  ;        /        ,--.........,
      |; ;  ;  ;  ;/       ;       .'           -='.
      | ;  ;  ; ; /       /       .\               '
      |  ;   ;  /`      .\   _,=="  \             .'
      \;  ; ; .'. _  ,_'\.\~"   //`. \          .'
      |  ;  .___~' \ \- | |    /,\ `  \      ..'
    ~ ; ; ;/  =="'' |`| | |       =="''\.==''
    ~ /; ;/=""      |`| |`|   ==="`
    ~..==`     \\   |`| / /=="`
     ~` ~      /,\ / /= )")
    ~ ~~         _')")  
    ~ ~   _,=~";`
    ~  =~"|;  ;|       Penisbird
     ~  ~ | ;  |       =========
  ~ ~     |;|\ |
          |/  \|


Single threaded, I will update this maybe, someday but probably not.

To change the amount of pages scraped per host (domain) edit:

line 60 of scraper py with: 
pbar2 = tqdm(desc='while loop', total=[TOTAL AMOUNT YOU WANT TO CHANGE HERE], position=1, leave=False)

and

line 97 of scraper.py with:
if cntr >= [SAME AMOUNT DEFINED ABOVE, HERE AS WELL]:


====== Txt files associated with script ======

scraped_emails.txt is an uncleaned original list of perceieved email data.
final_scraped_emails.txt is the clensed list from scraped_emails.txt
