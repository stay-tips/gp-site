---

########################### hero slider ############################
hero_slider:
  enable : true
  slider_item:
    # slider item
    - subtitle : "The values you can count on"
      title : "Hospitality"
      content : "Every property tells a unique story, woven into the vibrant fabric of the city that surrounds it. We take care of every detail to turn each stay into an authentic and memorable experience, bringing out the essence of every property and its surroundings."
      bg_image_webp : "images/slider/banner-1.webp"
      bg_image : "images/slider/banner-1.jpg"
      animation : "fadeInUp" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "learn more"
        link : "contact/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "The method that delivers results"
      title : "Professionalism"
      content : "We have perfected every stage of property management through processes designed down to the smallest detail. Our method combines hands-on experience with technological innovation to maximize both guest comfort and the profitability of your property. The result? Properties always at their best and property owners with peace of mind."
      bg_image_webp : "images/slider/banner-2.webp"
      bg_image : "images/slider/banner-2.jpg"
      animation : "fadeInDown" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "learn more"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "An innovative approach"
      title : "Sustainability"
      content : "Our approach to short-term rentals is built on values of sustainability and respect for the local area. We promote conscious tourism that showcases local excellence, creating a positive impact on the communities that host us."
      bg_image_webp : "images/slider/banner-3.webp"
      bg_image : "images/slider/banner-3.jpg"
      animation : "fadeInLeft" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "learn more"
        link : "about/"
        animation : "zoomIn" # animation select from : https://daneden.github.io/animate.css/
        
    # slider item
    - subtitle : "Guaranteed"
      title : "Maximum Return"
      content : "Only by achieving the maximum return on a property can we promote our values and share our happiness with guests"
      bg_image_webp : "images/slider/banner-4.webp"
      bg_image : "images/slider/banner-4.jpg"
      animation : "fadeInRight" # animation select from : https://daneden.github.io/animate.css/
      button:
        enable : true
        label : "learn more"
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
    - name : "Experiences"
      icon : "fas fa-horse" # font-awesome 5 : https://fontawesome.com/icons/
      content : "we let you experience the local area like a native"
      
    # banner feature item loop
    - name : "Hospitality"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      content : "welcoming homes to make you feel at home"
      
    # banner feature item loop
    - name : "Services"
      icon : "fas fa-shuttle-van" # font-awesome 5 : https://fontawesome.com/icons/
      content : "we cover every special need"


################################## about ####################################
about:
  enable : true
  subtitle : "A skilled and professional team"
  title : "A team at your service"
  content : "Your property will become a unique and highly profitable experience. You will see the value of your property grow steadily thanks to our professional and passionate management. You will finally be able to enjoy your real estate investments stress-free, with concrete and guaranteed results."
  bg_image : "images/backgrounds/about-us-bg.png"
  bg_image_webp : "images/backgrounds/about-us-bg.webp"
  image_webp : "images/about/about-us.webp"
  image : "images/about/about-us.png"
  button:
    enable : true
    label : "contact us"
    link : "contact/"

################################## funfacts ###############################
funfacts :
  enable : true
  funfacts_item :      

    # fanfacts item loop
    - name : "Years of experience"
      count : "5"
      icon : "far fa-calendar-alt" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Properties managed"
      count : "36"
      icon : "fas fa-house-user" # font-awesome 5 : https://fontawesome.com/icons/
      
    # fanfacts item loop
    - name : "Satisfied Guests"
      count : "5300"
      icon : "far fa-smile" # font-awesome 5 : https://fontawesome.com/icons/


################################# feature ############################################
feature:
  enable : true
  subtitle : "The 7 Virtues method"
  title : "A proven method"
  image_webp : "images/feature/activities.webp"
  image : "images/feature/activities.png"
  content : "Your property will generate more revenue with less stress and zero risk"
  feature_item:

    # Selezione Immobili
    - name : "We select only quality properties"
      icon : "fas fa-medal"
      content : "Not all properties are suited to short-term rentals. We select only properties with unique features and high income potential."
    
    # Allestimento
    - name : "Your property, irresistible"
      icon : "fas fa-camera"
      content : "Your property will become the most sought-after thanks to emotional staging crafted down to the smallest detail, along with professional photos and videos."

    # Burocrazia
    - name : "Zero bureaucratic worries"
      icon : "fas fa-landmark"
      content : "Regulations, formalities, notifications, deadlines: managing a holiday home is a bureaucratic maze, and a single mistake is costly. We take care of everything so you don't have to think about it."
 
    # Pulizia
    - name : "A property always in perfect condition"
      icon : "fas fa-broom"
      content : "Your property will always be impeccable and kept in the best condition, preserving its value over time."

    # Accoglienza
    - name : "Satisfied guests, top reviews"
      icon : "fas fa-hand-holding-heart"
      content : "Your guests will enjoy a memorable experience, earning you excellent reviews and continuous bookings"

    # Partner selezionati
    - name : "Network of selected partners"
      icon : "fas fa-handshake"
      content : "If guests want an extra service, we can accommodate them, promoting the local area and local culture"

    # Gestione Prezzi
    - name : "Maximum revenue guaranteed by contract"
      icon : "fas fa-chart-line"
      content : "You will earn the most possible from every night, thanks to revenue management and smart pricing, and if we don't reach the targets we'll refund you the difference"


################################# advantages ############################################
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
    enable : false
    label : "more case studies"
    link : "project/"
  # project item comes from "content/*/project" folder

################################# testimonial #########################################
testimonial:
  enable : true
  subtitle : "Testimonials"
  title : "What do clients say?"
  testimonial_item:
    # testimonial item loop
    - client_image : "images/testimonial/client-1.webp"
      name : "Elisa"
      designation : "Property owner"
      content : "Enrico proved to be knowledgeable and attentive, and he found the right tax structure to make my property as profitable as possible. Keep it up"
      
    # testimonial item loop
    - client_image : "images/testimonial/client-2.webp"
      name : "Renato"
      designation : "Property owner"
      content : "Enrico and his team manage short-term rentals with method and availability. Thanks to them I put my home on the market in 2 weeks. Thank you."

    # testimonial item loop
    - client_image : "images/testimonial/client-3.webp"
      name : "Alessandra"
      designation : "Property owner"
      content : "In managing guests, Green Property has shown warmth and professionalism. With reviews almost always above 9, the value of the business has gone up."

    # testimonial item loop
    - client_image : "images/testimonial/client-4.webp"
      name : "Davide"
      designation : "Property owner"
      content : "With Green Property, managing my property runs like clockwork: check-ins, cleaning and maintenance all flow smoothly without me having to think about it. Real efficiency."


################################# cta ################################################
cta:
  enable : true
  title : "Your property will reach its full potential in the tourism and hospitality sector"
  bg_image_webp : "images/backgrounds/cta-lg.webp"
  bg_image : "images/backgrounds/cta-lg.jpg"
  button:
    enable : true
    label : "find out how much your property is worth"
    link : "contact/"

################################# blog ################################################
blog:
  enable : true
  section : "blog"
  show_item : 3
  # blog post comes from "content/*/blog" folder

---
