---

########################### hero slider ############################
hero_slider:
  enable : true
  slider_item:
    # slider item
    - subtitle : "i valori su cui puoi contare"
      title : "Ospitalità"
      content : "Valorizzando le unicità dell'immobile e dei suoi dintorni, assicurando agli ospiti un soggiorno sereno e memorabile."
      bg_image_webp : "images/slider/banner-1.webp"
      bg_image : "images/slider/banner-1.jpg"
      animation : "fadeInUp" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "contact/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Il metodo che ti assicura risultati"
      title : "Professionalità"
      content : "Abbiamo ingegnierizzato processi unici per garantire il massimo del confort e del rendimento dell'immobile."
      bg_image_webp : "images/slider/banner-2.webp"
      bg_image : "images/slider/banner-2.jpg"
      animation : "fadeInDown" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Un approcio innovativo"
      title : "Sostenibilità"
      content : "Crediamo nel turismo etico e responsabile, che rispetti l'ambiente circostante e promuova prodotti e abitudini del territorio, negli affitti brevi"
      bg_image_webp : "images/slider/banner-3.webp"
      bg_image : "images/slider/banner-3.jpg"
      animation : "fadeInLeft" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Garantito"
      title : "Massimo Rendimento"
      content : "Solo raggiungendo il massimo rendimento dell'immobile possiamo promuovere i nostri valori e condividere con gli ospiti la nostra felicità"
      bg_image_webp : "images/slider/banner-4.webp"
      bg_image : "images/slider/banner-4.jpg"
      animation : "fadeInRight" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "approfondisci"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/

################################## banner feature ############################
banner_feature:
  enable : true
  # Max use 4 item
  feature_item:

    # banner feature item loop
    # - name : "Business Solution"
    #   icon : "far fa-gem" # font-awesome 5 : https://fontawesome.com/icons/
    #   content : "Lorem ipsum dolor sit amet constur adipelit sed."
      
    # banner feature item loop
    - name : "Epserienze"
      icon : "fas fa-horse" # font-awesome 5 : https://fontawesome.com/icons/
      content : "facciamo vivere il territorio come nativi"
      
    # banner feature item loop
    - name : "Ospitalità"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      content : "accoglienti dimore per sentirsi casa"
      
    # banner feature item loop
    - name : "Servizi"
      icon : "fas fa-shuttle-van" # font-awesome 5 : https://fontawesome.com/icons/
      content : "copriamo ogni necessità particolare"


################################## about ####################################
about:
  enable : true
  subtitle : "Un team preparato e professionale"
  title : "Una squadra al tuo servizio"
  content : "Il tuo immobile diventerà un'esperienza unica e altamente redditizia. Vedrai il valore della tua proprietà crescere costantemente grazie alla nostra gestione professionale e appassionata. Potrai finalmente goderti i tuoi investimenti immobiliari senza stress, con risultati concreti e garantiti."
  bg_image : "images/backgrounds/about-us-bg.png"
  bg_image_webp : "images/backgrounds/about-us-bg.webp"
  image_webp : "images/about/about-us.webp"
  image : "images/about/about-us.png"
  button:
    enable : true;
    label : "contattaci"
    link : "service/"

################################## funfacts ###############################
funfacts :
  enable : true
  funfacts_item :      

    # fanfacts item loop
    - name : "Anni d'esperienza"
      count : "5"
      icon : "far fa-calendar-alt" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Immobili gestiti"
      count : "16"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Ospiti Soddisfatti"
      count : "5300"
      icon : "far fa-smile" # font-awesome 5 : https://fontawesome.com/icons/


################################# feature ############################################
feature:
  enable : true
  subtitle : "Il metodo 7 Virtues"
  title : "Un metodo collaudato"
  image_webp : "images/feature/activities.webp"
  image : "images/feature/activities.png"
  content : "Il tuo immobile genererà più ricavi con meno stress e zero rischi"
  feature_item:
    # Business plan
    - name : "Ricavi Garantiti"
      icon : "fas fa-money-bill"
      content : "Riceverai un piano dettagliato che mostra quanto potrai guadagnare dall'immobile e se non raggiungiamo gli obiettivi rimborsiamo la provvigione."
    
    # Allestimento
    - name : "Il tuo immobile irresistibile"
      icon : "fas fa-camera"
      content : "La tua proprietà diventerà la più desiderata online grazie a foto e video professionali e allestimenti curati."

    # Burocrazia
    - name : "Zero pensieri burocratici"
      icon : "fas fa-landmark"
      content : "Non dovrai più preoccuparti di pratiche, scadenze o normative - pensiamo a tutto noi."
 
    # Pulizia
    - name : "Immobile sempre perfetto"
      icon : "fas fa-broom"
      content : "La tua proprietà sarà sempre impeccabile e mantenuta al meglio, preservando il suo valore nel tempo."

    # Accoglienza
    - name : "Ospiti soddisfatti, recensioni top"
      icon : "fas fa-hand-holding-heart"
      content : "I tuoi ospiti vivranno un'esperienza memorabile, garantendoti recensioni eccellenti e prenotazioni continue"

    # Gestione Prezzi
    - name : "Massimi ricavi sempre"
      icon : "fas fa-chart-line"
      content : "Guadagnerai il massimo possibile da ogni notte, grazie alla gestione dei prezzi smart."

    # Partner selezionati
    - name : "Rete di partner selezionati"
      icon : "fas fa-handshake"
      content : "Se gli ospiti desiderano un servizio extra possiamo accontentarli, promuovendo il territorio e la cultura locale"


################################# service ############################################
service:
  enable : true
  section: "service"
  show_item : 8
  # service item comes from "content/*/service" folder

################################# team ##############################################
team:
  enable : true
  section: "team"
  show_item : 3
  # team member comes from "content/*/team" folder

################################# project ############################################
project:
  enable : true
  section: "project"
  show_item : 4
  button:
    enable : true
    label : "altri casi studio"
    link : "project/"
  # project item comes from "content/*/project" folder

################################# testimonial #########################################
testimonial:
  enable : true
  subtitle : "Testimonianze"
  title : "Cosa dicono i clienti?"
  testimonial_item:
    # testimonial item loop
    - client_image : "images/testimonial/client-1.jpg"
      name : "Elisa"
      designation : "Proprietario"
      content : "Enrico si è dimostrato preparato attento e ha trovato la struttura fiscale giusta per far rendere il mio immobile al massimo, avanti così"
      
    # testimonial item loop
    - client_image : "images/testimonial/client-2.jpg"
      name : "Renato"
      designation : "Proprietario"
      content : "Enrico e i suoi collaboratori gestiscono gli affitti brevi con metodo e disponibilità. grazie a loro ho messo sul mercato la mia casa in 2 settimane. Grazie."

    # testimonial item loop
    - client_image : "images/testimonial/client-3.jpg"
      name : "Alessandra"
      designation : "Proprietario"
      content : "Nella gestione degli ospiti, Green Property ha dimostrato accoglienza e professionalità. Dalle recensioni quasi sempre sopra il 9 il valore dell'attività è salito."


################################# cta ################################################
cta:
  enable : true
  title : "Il tuo immobile raggiungerà il massimo potenziale nell'ospitalità turistico-ricettiva"
  bg_image_webp : "images/backgrounds/cta-lg.webp"
  bg_image : "images/backgrounds/cta-lg.jpg"
  button:
    enable : true
    label : "chiedi una valutazione gatuita"
    link : "contact/"

################################# blog ################################################
blog:
  enable : true
  section : "blog"
  show_item : 3
  # blog post comes from "content/*/blog" folder

---
