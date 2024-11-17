$(function(){
    init();
});

function init() {
    if($('.hero-carousel').length > 0){
        $('.hero-carousel').slick({
            arrows: false,
            autoplay: true,
            autoplaySpeed: 6000,
            speed: 1000
        });
    }
    if($('.locations-carousel').length > 0){
        $('.locations-carousel').slick({
            arrows: false,
            slidesToShow: 2,
            slidesToScroll: 1,
            infinite: false
        });
    }
    if($('.reviews-carousel').length > 0){
        $('.reviews-carousel').slick({
            arrows: false,
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: false,
            dots: true,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                },
            ]
        });
    }
    if($('#chisiamo-second-section').length > 0){
        heroCorrection();
        $(window).resize(function(){
            heroCorrection();
        });
    }

    function heroCorrection(){
        var margintop = $('.hero-second.chisiamo').offset().top + $('.hero-second.chisiamo').height();
        if($('#chisiamo-second-section').offset().top < margintop){
            console.warn('true');
            $('#chisiamo-second-section').css('padding-top', (margintop - $('#chisiamo-second-section').offset().top + 64));
        }
    }

    if($('.more').length > 0){
        $('.more').each(function(){
            if($(this).parent().parent().find('.description p').height() < 152){
                $(this).addClass('d-none');
                $(this).parent().addClass('py-2');
            }
        });
    }
}

function readMore(button){
    $(button).parent().parent().find('.description').css('max-height', '500px');
    $(button).attr('onclick', 'readLess(this)').text('Read less');
}

function readLess(button){
    $(button).parent().parent().find('.description').css('max-height', '152px');
    $(button).attr('onclick', 'readMore(this)').text('Read more');
}

function addautoplay(src){
    console.warn(src);
    document.getElementById('video-iframe').setAttribute('src', src+'?fs=1&autoplay=1&mute=1&loop=1');
    document.getElementById('exampleModalCenter').classList.add('fade');
}

function removeautoplay(){
    document.getElementById('video-iframe').setAttribute('src', '');
    document.getElementById('exampleModalCenter').classList.remove('fade');
}