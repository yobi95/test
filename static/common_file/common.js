/* =================================================================================================
 common.js
 > store general scripts which would be used on multiple templates
 
 * @TODO Simplify
 ================================================================================================= */

// ========================
// Common Variables
// ========================
var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var windowHeight = $(window).height();
var windowJsOldWidth, windowJsOldHeight;   //Used to detect unexpected trigger on window resize
var lang = document.documentElement.lang;
var isChrome, isFirefox, isSafari, isEdge, isIE, isMSTouchDevice;
var scrollTop = 0;
var $body = $('body');
var $header = $('header');
var $footer = $('footer');
var headerHeight = 0, footerHeight = 0;
var isHome = false;
var modeDev = false;    //toggle dev mode (test mode)

// Layout or content related variables
var aniElemPos = []; //Store position for scrolling effects
var cmErrMsgSamples = '';   //Stores Field Error Msgs
var formErrMsgSamples = '';    //Stores Form Error Msgs
var resizeTimer;
var scrollTimer;
// ========================

// ========================
// Page-specific variables
// ========================
var playButtonTimer;

// ========================

$(document).ready(function () {
    $body = $('body'), $header = $('header'), $footer = $('footer');
    lang = document.documentElement.lang;
    isHome = $body.hasClass('page-home');
    init();
    $body.addClass('page-ready');
});

$(window).on('load', function () {
    resize(true);
    $body.addClass('page-ready');
    //$('.ani').removeClass('in-view');
    $(window).scroll();
});

$(window).on('resize', _.debounce(function () {
    resize();
}, 150));


$(window).on('scroll', _.throttle(function () {
    scroll();
}, 250));

function scrollToElemTop($elem, time) {
    if (!time) {
        time = 1000;
    }
    $('html, body').animate({
        'scrollTop': $elem.offset().top - $header.outerHeight()
    }, time);
}

function setGlobalVar() {
    scrollTop = $(document).scrollTop();
    windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    windowHeight = $(window).height();
    headerHeight = $header.outerHeight() || 0;
    footerHeight = $footer.outerHeight() || 0;
}

function init() {
    setGlobalVar();

    // High priority in execution
    //...TO BE FILLED

    // Browser or devices related
    checkEnvironment();

    // Common
    commonBehaviour();


    // Pages or sections specfic
    initMainBanner();
    initVideoModal();
    fixVideoTagOnAndroidStockBrowser();
    initChangePwForm();

    // Action or triggers
    $(window).scroll();
    resize(true);
    handleHash();
    burgerMenu();
    menuChange();
    submenuChange();
    profileLogin();
    mobileMenu();
    searchOverlay();
    scrollTransition();
    emptyInput();
    collapsibleBox();
    allChecked();
    scrollFixed();
    videoThumb();
    tabOpen();
    //gifReplay();
    imageLink();
    initStatChart();
    // Run lastly
    //...TO BE FILLED
}
function resize(initMode) {
    setGlobalVar();
    if (initMode) {
        //...TO BE FILLED
    } else {
        if (resizeTimer) {
            clearTimeout(resizeTimer);  // Reset timer
        }
        // Add a class "is-resizing" to body when resizing
        $body.addClass('is-resizing');
        resizeTimer = setTimeout(function () {
            $body.removeClass('resizing');
        }, 50);
    }
    //handleMain();

    if (windowJsOldWidth != windowWidth) {
        windowJsOldWidth = windowWidth;
        // Will run only for WIDTH Resize:
    }
}
function scroll() {
    scrollTop = $(document).scrollTop();
    //handleFixedMenu();
    if (scrollTimer) {
        clearTimeout(scrollTimer);  // Reset timer
    }
    // Add a class "is-scrolling" to body when scrolling
    $body.addClass('is-scrolling');
    scrollTimer = setTimeout(function () {
        $body.removeClass('is-scrolling');
    }, 250);
}
// ========================
// Init functions
// ========================
function initChangePwForm(){
    var $assignmentForm = $('#assignmentForm');
    if (!$assignmentForm.length) {
        return false;
    }
    var ajaxPath = hostPath + 'changePw.php';
    var assignmentFormElem = $assignmentForm.get(0);
    var $submitBtn = $assignmentForm.find('[type="submit"]');
    $submitBtn.click(function(e){
        e.preventDefault();
            if (validateForm(assignmentFormElem)) {
                $submitBtn.addClass('btn--loading');
                $.ajax({
                    url: ajaxPath,
                    type: 'POST',
                    dataType: 'json',
                    data: $assignmentForm.serialize(),
                    cache: false
                }).done(function (data) {
                    if (data) {
                      if (data.status == 'S') {
                          //success
                          alert(getTxtByLang(['Password changed successfully', '密碼成功更改', '密码成功更改']));
                          $assignmentForm.find('input').val('');
                          location.href = '/' + $lang + '/member/login-dashboard.php';
                      } else if (data.status == 'F') {
                          //fail
                          alert(getTxtByLang(['Incorrect current password', '現時密碼輸入錯誤', '现时密码输入错误']));
                      } else if (data.status == 'F1') {
                          alert(getTxtByLang(['Fail to change password', 'Fail to change password', 'Fail to change password']));
                      } else if (data.status == 'INVALID_LENGTH') {
                          alert(getTxtByLang(['Invalid password length', '密碼長度不符', '密码长度不符']));
                      } else if (data.status == 'F-DUP') {
                          alert(getTxtByLang(['New password cannot duplicate with recently old password', '新密碼不能與最近使用過的舊密碼重覆', '新密码不能与最近使用过的旧密码重覆']));
                      }
                    }
                });
            }
    });
}
function initMainBanner() {
    var $mainBanner = $('.main-banner');
    if (!$mainBanner.length) {
        return false;
    }
    $mainBanner.each(function () {
        var $thisMainBanner = $(this);
        var $mainBannerSlider = $thisMainBanner.find('.main-banner__slider')[0];
        var nextEl = $thisMainBanner.find('.main-banner__slider-next')[0];
        var prevEl = $thisMainBanner.find('.main-banner__slider-prev')[0];
        var pagination = $thisMainBanner.find('.main-banner__pagination')[0];
        var thisSwiper = new Swiper($mainBannerSlider, {
            slidesPerView: 1,
            slidesPerGroup: 1,
            loop: true,
            observer: true,
            paginationClickable: true,
            autoplayDisableOnInteraction: false,
            simulateTouch: true,
            observeParents: true,
            init: false,
            effect: 'fade',
            autoplay: {
              delay: 5000,
            },
            navigation: {
                nextEl: nextEl,
                prevEl: prevEl
            },
            pagination: {
                el: pagination,
                type: 'bullets',
                clickable: true,
                renderBullet: function (index, className) {
                    var txtSlide = getTxtByLang(['To slide no. ' + (index + 1), '去第' + (index + 1) + '張', '去第' + (index + 1) + '张']);
                    return '<a href="#" class="' + className + '" title="' + txtSlide + '">' + '</a>';
                }
            },
            fadeEffect: {
                crossFade: true
              },
        });

        thisSwiper.on('init', function () {
            initSwiperPause($mainBanner, thisSwiper);
        });
        thisSwiper.init();
    });
}

function initSwiperPause($holder, swiper) {
    var $pauseBtn = $holder.find('.swiper-button-pause');
    $pauseBtn.unbind().click(function (e) {
        e.preventDefault();
        var $thisPauseBtn = $(this);
        if (!$holder.hasClass('swiper-paused')) {
            $holder.addClass('swiper-paused');
            swiper.autoplay.stop();
            var txtPause = getTxtByLang(['Play', '播放', '播放']);
            var txtPauseAccess = '<span class="access">' + txtPause + '</span>';
            $thisPauseBtn.attr('title', txtPause);
            $thisPauseBtn.html(txtPauseAccess);
        } else {
            $holder.removeClass('swiper-paused');
            swiper.autoplay.start();
            var txtPause = getTxtByLang(['Pause', '暫停', '暂停']);
            var txtPauseAccess = '<span class="access">' + txtPause + '</span>';
            $thisPauseBtn.attr('title', txtPause);
            $thisPauseBtn.html(txtPauseAccess);
        }
    });
}

function initVideoModal(){
    var $videoModalBtn = $('.js-modal-btn');
    if (!$videoModalBtn.length) {
        return false;
    }
    $videoModalBtn.modalVideo();
}

function fixVideoTagOnAndroidStockBrowser() {
    const ua = window.navigator.userAgent.toLowerCase();;
    const isStock = 
        ua.indexOf('samsung') != -1 || 
        ua.indexOf('nexus') != -1;

    $videoElm = $('.page-fps .image-holder video');

    if(isStock && $videoElm.length > 0) {
        $videoElm.addClass('pause');
        $videoElm.removeAttr('autoplay');
        $videoElm.removeAttr('controls');
        
        var $btn_pause = $('<a/>', {
            class: 'btn-pause'
        });
        $btn_pause.html('&nbsp;');
        $videoElm.parent().append($btn_pause);

        $videoElm.parent().hover(function() {
            showVideoPlayButton($btn_pause, true);
        }, function () {
            if(!$videoElm.hasClass('pause')) {
                showVideoPlayButton($btn_pause, false);
            }
        });

        $btn_pause.click(function() {
            $videoElm.toggleClass('pause');

            if($videoElm.hasClass('pause')) {
                $videoElm.trigger('pause');
                $btn_pause.html('&nbsp;');
            }
            else {
                $videoElm.trigger('play');
                $btn_pause.html('||');
            }
        })

        $(document).click(function(e) {
            var $img_holder = $videoElm.parent();
            if (!$img_holder.is(e.target) && $img_holder.has(e.target).length === 0) {
                if(!$videoElm.hasClass('pause')) {
                    $btn_pause.fadeOut();
                } 
            }
        })
    }
}

function showVideoPlayButton($btn_pause, show)
{
    if (show) {
        $btn_pause.stop().fadeIn();
        $btn_pause.addClass('show');
    }
    else {
        $btn_pause.stop().fadeOut();
        $btn_pause.removeClass('show');
    }
}

function videoThumb(){
    var $elm = $('.video-thumb');
    
    $elm.each(function(){
        var $this = $(this),
            $videoID = $this.attr('data-video-id');
            src1 = 'https://img.youtube.com/vi/' + $videoID +'/0.jpg'

        $this.children('img').attr('src', src1)
    })
}

// ========================
// Layout Handlers
// ========================

function handleMain() {
    var $main = $('main');
    if (!$main.length) {
        return false;
    }
    var minHeight = windowHeight - headerHeight;
    $main.css({
        'min-height': minHeight + 'px'
    });


}
/*function handleFixedMenu() {
    if (scrollTop > 50) {
        $body.addClass('header--small');
    } else {
        $body.removeClass('header--small');
    }
}*/

function scrollTransition() {
    $(window).scroll(_.throttle(function () {
        var $scrollTop = $(window).scrollTop();
        var $elm = $('.js-animated');
   
        $elm.each(function(){
            var $this = $(this),
                $animation = $this.attr('data-animation');
                $windowHeight = $(window).height();
                $delay = $this.attr('data-delay');

            if( $scrollTop > $this.offset().top - $windowHeight){
                setTimeout(function(){
                    $this.addClass($animation);
                }, $delay);
            }
        });
   
   },100));
}
// Action Handlers
// ========================
function handleHash() {
    var hashTag = window.location.hash;
    if (hashTag && hashTag != '#') {
        if ($(hashTag + ':visible').length) {
            var offset = 0;
            var $submenu = $('.sub-menu');
            if ($submenu.length) {
                $('html, body').animate({
                    'scrollTop': $(hashTag).offset().top - $('header').outerHeight() - $('.sub-menu').outerHeight()
                }, 1000);
            } else {
                $('html, body').animate({
                    'scrollTop': $(hashTag).offset().top - $('header').outerHeight()
                }, 1000);
            }
        }
    }
}

function commonBehaviour(){
    $('.no-link').click(function(event){
        event.preventDefault(event);
    })
}
function emptyInput(){
    setTimeout(function(){
        $('input:text').val('');
    }, 300)
}
function burgerMenu() {
    $('.burger').click(function(){
        $('.bar-1, .bar-2, .bar-3').toggleClass('active');
        $('.mobile-shade').stop().slideToggle();
        $('body').toggleClass('no-overflow');

        setTimeout(function(){
            $('.mobile-nav__link, .mobile-nav__btm').removeClass('disable');
            $('.mobile-nav__top, .mobile-nav__btm, .mobile-nav__sub').removeClass('active');
            $('.mobile-nav__sub-inner').slideUp();
            }, 300);
    })
    $(window).resize(function(){
        if ( $(window).width() > 991 ) {
            $('.mobile-shade').fadeOut();
            $('.bar-1, .bar-2, .bar-3').removeClass('active');
            $('body').removeClass('no-overflow');
        }
    })
}
function mobileMenu() {
    $('.mobile-nav__link').click(function(){
        $('.mobile-nav__link, .mobile-nav__btm').addClass('disable');
        $('.mobile-nav__sub').removeClass('active');
        $(this).next().addClass('active');
    })
    $('.mobile-nav__link.hv-sub').click(function(){
        $('.mobile-nav__top, .mobile-nav__btm').addClass('active');
    })
    $('.mobile-nav__back').click(function(){
        $('.mobile-nav__link, .mobile-nav__btm').removeClass('disable');
        $('.mobile-nav__top, .mobile-nav__btm, .mobile-nav__sub').removeClass('active');
    })
    $('.mobile-nav__sub .hv-sub').click(function(){
        $('.mobile-nav__sub-inner').stop().slideUp();
        $(this).next().stop().slideToggle();
    })
}

function menuChange() {
    var $elm = $('.header-nav__link.hv-sub');
        $elm.addClass('tab_open');

    $('.header-nav__sub, .header-nav__link').on('touchstart', function(){
        event.stopPropagation();
    })
    
    $elm.on('touchstart', function(e){
        var $this = $(this);
        if ($(this).hasClass('tab_open')){
            e.preventDefault();
            $('.btn-profile__popup').fadeOut(100, 'swing');
            $('.btn-profile').removeClass('active');
            $('.btn-search-popup').stop().slideUp();
            emptyInput();
            $('.header-nav__sub').css('z-index', '0').removeClass('acitve').stop().slideUp()
            $(this).siblings('.header-nav__sub').addClass('acitve').css('z-index', '999').stop().slideDown();
            $elm.addClass('tab_open');
            $this.toggleClass('tab_open');
        } else {
        }
    })
    $('.header-nav__link').mouseover(function(e){
        $('.header-nav__sub').css('z-index', '0').removeClass('acitve').stop().slideUp();
        $(this).siblings('.header-nav__sub').addClass('acitve').css('z-index', '999').stop().slideDown();
        emptyInput();
    })
    $('.header-nav__sub').mouseleave(function(){
        $('.header-nav__sub').removeClass('acitve').stop().slideUp();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
        $elm.addClass('tab_open');
    })
    $(document).on('touchstart', function(){
        $('.header-nav__sub').removeClass('acitve').stop().slideUp();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
        $elm.addClass('tab_open');
    })
}

function submenuChange() {
    var $elm = $('.header-nav__sub-right .hv-sub');
        $elm.addClass('submenu_open');
    
    $elm.on('touchstart', function(e){
        var $this = $(this);
        if ($(this).hasClass('submenu_open')){
            e.preventDefault();
            $('.header-nav__sub-right-inner').stop().fadeOut();
            $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
            $(this).css('color', 'rgba(255,255,255,0.5').next().stop().fadeIn();
            $elm.addClass('submenu_open');
            $this.toggleClass('submenu_open');
        } else {
        }
    })
    $('.header-nav__sub-right .hv-sub').mouseover(function(){
        $('.header-nav__sub-right-inner').stop().fadeOut();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
        $(this).css('color', 'rgba(255,255,255,0.5').next().stop().fadeIn();
    })
    $('.header-nav__sub-right a').not('.hv-sub, .header-nav__sub-right-inner a').mouseover(function(){
        $('.header-nav__sub-right-inner').stop().fadeOut();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
    })
    $('.header-nav__sub-right a').not('.hv-sub, .header-nav__sub-right-inner a').mouseleave(function(){
        $('.header-nav__sub-right-inner').fadeOut();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
    })
    $('.header-nav__sub').mouseleave(function(){
        $('.header-nav__sub-right-inner').stop().fadeOut();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
    })
}
function profileLogin() {
    $('.btn-profile').click(function(){
        var $this = $(this);
        if (!$(this).hasClass('active')){
            $this.addClass('active');
            $('.header-nav__sub').removeClass('acitve').stop().slideUp();
            $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
            $('.btn-search__popup').fadeOut(100, 'swing');
            $('.btn-search-popup').stop().slideUp();
            $('.btn-profile__popup').fadeIn(100, 'swing');
        } else {
            $this.removeClass('active');
            $('.btn-profile__popup').fadeOut(100, 'swing');
            emptyInput();
        }
    })

    $(document).click(function(e) {
        var login_btn = $('.btn-profile');
        var popup = $('.btn-profile__popup');
        if (!login_btn.is(e.target) && !popup.is(e.target) && popup.has(e.target).length === 0) {
            login_btn.removeClass('active');
            popup.fadeOut(100, 'swing');
            emptyInput();
        }
    })
}
function searchOverlay() {
    $('.btn-search').click(function(){
        $('.btn-profile__popup').fadeOut(100, 'swing');
        $('.header-nav__sub').removeClass('acitve').stop().slideUp();
        $('.header-nav__sub-right .hv-sub').css('color', 'rgba(255,255,255,1');
        $('.btn-search-popup').stop().slideToggle();
        $('.btn-search-popup .search-input').focus();
    })

    $(document).click(function(e) {
        var search_btn = $('.btn-search');
        var popup = $('.btn-search-popup');
        if (!search_btn.is(e.target) && !popup.is(e.target) && popup.has(e.target).length === 0) {
            popup.stop().slideUp();
        }
    })
}
function collapsibleBox(){
    var $elm = $('.collapsible-box').first();

    $elm.children('.collapsible-box__title').addClass('active').siblings('.collapsible-box__content-wrapper').slideDown();

    $('.collapsible-box__title').click(function(){
        $(this).toggleClass('active').siblings('.collapsible-box__content-wrapper').stop().slideToggle();
    })

    $('.collapsible-btn__show').click(function(){
        $('.collapsible-box__title').addClass('active');
        $('.collapsible-box__content-wrapper').stop().slideDown();
    })

    $('.collapsible-btn__hide').click(function(){
        $('.collapsible-box__title').removeClass('active');
        $('.collapsible-box__content-wrapper').stop().slideUp();
    })
}
function allChecked(){
    $('input.check-all').click(function(){
        if (this.checked){
            $('input[name="currency"]').each(function(){
                this.checked = true;
            })
        } else {
            $('input[name="currency"]').each(function(){
                this.checked = false;
            })
        }
        $('input[name="currency"]').not('.check-all').click(function(){
            $('input.check-all').each(function(){
                this.checked = false;
            })
        })
    })
}
function scrollFixed(){
    var $stickyEl, $stickyElParent, $navSticky, navStickyHeight;
    var $stickyEls = $('.scroll-sticky');
    var $containers = $stickyEls.parent().parent();
    var containerIsActive = false;
    var navStickyBuffer = 0;
    var containerBufferBottom = 0;
    var lastY = 0;

    $stickyEl = $('.scroll-sticky');
    $stickyElParent = $stickyEl.parent().parent();
    $navSticky = $('header');
    navStickyHeight = $navSticky.height() + navStickyBuffer;

    if ($(window).width() > 991) {

        $(window).on('scroll', function(){
            currentScrollY = window.scrollY;
            //Get the direction of the scroll (negative = up or positive = down)
            var delta = currentScrollY - lastY;
                lastY = currentScrollY;
            var $activeContainer = $containers.filter('.active');
            var $containersSubset = $containers;

            if ($activeContainer.length) {
                // if active container exists, check if still active
                checkActiveContainer($activeContainer, currentScrollY);
                // if active container is still active, break out of function
                if (containerIsActive === true) {
                    return;
                }
                // if active container exists but is not still active,
                // create subset of potentially active sections to check if active
                if ($containers.length > 2) {
                    var activeContainerIndex = $containers.index($activeContainer);
                    // if upwards scroll, create subset with those preceding former active section
                    // if downwards scroll, create subset with those following former active section
                    if (delta < 0 ){
                    $containersSubset = $containers.slice(0, activeContainerIndex - 1);
                    } else {
                    $containersSubset = $containers.slice(activeContainerIndex - 1);
                    }
                }
            }
            // if no active container exists, or former active container is no longer active,
            // reset containers and ads to inactive state
            $containers.removeClass('active');
            $stickyEls.removeClass('sticky');
                
            // cycle through potentially active sections to check if active
            $containersSubset.each(function() {
                if (containerIsActive === false) {
                    checkActiveContainer($(this), currentScrollY);
                }
            })
        });

        function checkActiveContainer($container, currentScrollY) {
            // set top boundary of section
            var containerOffsetTop = $container.offset().top - navStickyHeight;
            // set bottom boundary of section
            var containerOffsetBottom = containerOffsetTop + $container.innerHeight() - containerBufferBottom;
            // if current scroll position is within bounds, section is active
            if (containerOffsetTop <= currentScrollY && currentScrollY <= containerOffsetBottom) {
                containerIsActive = true;
                var $stickyEl = $container.find('.scroll-sticky');
                // find bottom bound of scroll boundary area
                var scrollBoundary = $container.innerHeight() - $stickyEl.innerHeight() - containerBufferBottom;
                $container.not('.active').addClass('active');
                // check if boundary area is tall enough to accommodate sticky el height
                if (scrollBoundary > 0) {
                    if (currentScrollY > containerOffsetTop + scrollBoundary) {
                        // if vert scroll position is outside scroll boundary area,
                        // sticky el is stuck (absolute position at bottom of boundary area)
                        $stickyEl.not('.stuck').removeClass('sticky').addClass('stuck');
                    } else {
                        // if vert scroll position is within scroll boundary area,
                        // sticky el is sticky (fixed position at bottom of nav)
                        $stickyEl.not('.sticky').addClass('sticky').removeClass('stuck');
                        $container.prev().find('.scroll-sticky').not('.stuck').addClass('stuck');
                    }
                }
            } else {
                containerIsActive = false;
            }
        }
    } if ($(window).width() < 991) {
        $stickyEls.css('position', 'initial');
    }
}

function tabOpen(){
    var $elm = $('.tab__each');

    $elm.each(function(){
        var $this = $(this),
            $appendAttr = $this.children().text();
        $this.attr('data-docu-type', $appendAttr);
    })

    $elm.click(function(){
        $elm.removeClass('selected');
        $(this).addClass('selected');

        var $this = $(this);
            $matchAttr = $this.attr('data-docu-type');
            $elem = $('.tab-content-wrapper');
            $toMatchAttr = $elem.attr('data-grp');

            $elem.each(function(){
                var $this = $(this); 
                    $toMatchAttr = $this.attr('data-grp');

                if ($matchAttr == $toMatchAttr) {
                    $elem.removeClass('active');
                    $this.addClass('active');
                }
            })
    })
}

function validateForm(assignmentForm) {
    var messages = [];
    var letterNumber = /^[0-9a-zA-Z]+$/;

    $('#assignmentForm').find('input').parent().removeClass('form-alert');
    if (document.assignmentForm.currentPassword.value=="") {
        messages.push("Please enter current password");
        $('#currentPassword').parent().addClass('form-alert');

    }
    if (document.assignmentForm.newPassword.value=="") {
        messages.push("Please enter new password");
        $('#newPassword').parent().addClass('form-alert');
    }
    if (document.assignmentForm.retypeNewPassword.value=="") {
        messages.push("Please enter retype new password");
        $('#retypeNewPassword').parent().addClass('form-alert');
    }
    if (document.assignmentForm.retypeNewPassword.value !== document.assignmentForm.newPassword.value) {
        messages.push("The new password is not equal to retype new password");
        $('#newPassword, #retypeNewPassword').parent().addClass('form-alert');
    }
    /*
    if (document.assignmentForm.newPassword.value.length < 8) {
        messages.push("Please fill in new password with at least 8 characters");
        $('#newPassword').parent().addClass('form-alert');
    }
    */
    if (document.assignmentForm.currentPassword.value == document.assignmentForm.newPassword.value) {
        messages.push("Please input a new password which is not equal to current password");
        $('#currentPassword, #newPassword').parent().addClass('form-alert');
    }
    /*
    if (!document.assignmentForm.newPassword.value.match(letterNumber)) {
        messages.push("Invalid character found, password should be 6 to 12 alpha numeric characters!");
        $('#newPassword').parent().addClass('form-alert');
    }
    */
    var newPassword = document.assignmentForm.newPassword.value;
    
		var pattNumberList = /[0-9]/;
		var pattAlphaList = /[a-zA-Z]/;
		var pattSpCharList = /[@$,.<>#:?_*&;]/;
    
    var patt = new RegExp(pattNumberList);
    if (!patt.test(newPassword))
    {
        messages.push("New password must contain at least one numeric character");
        $('#newPassword').parent().addClass('form-alert');
    }
    
    var patt = new RegExp(pattAlphaList);
    if (!patt.test(newPassword))
    {
        messages.push("New password must contain at least one alphabetic character");
        $('#newPassword').parent().addClass('form-alert');
    }
    
    var patt = new RegExp(pattSpCharList);
    if (!patt.test(newPassword))
    {
        messages.push("New password must contain at least one special character");
        $('#newPassword').parent().addClass('form-alert');
    }
    
    
    if (messages.length > 0) {
        alert(messages.join('\n'));
        formIsValid = false;
    } else {
         formIsValid = true;      
    }
    
    return formIsValid;
}

function gifReplay() {
    /*var $elm = $('.fps-one-col__each-content .image-holder, .content-right .image-holder');
        $elm.each(function(){
            var $this = $(this);
            $this.bind('mouseover touchstart', function(){
                var $thisAttr = $this.children().attr('src');
                $this.children().attr('src', $thisAttr);
        })
    })*/
    $('.gif').gifplayer();
}

function imageLink(){
    var $elm = $('.fps-one-col__each-content .image-holder img, .content-right .image-holder img');
        $elm.each(function (){
            var $this = $(this);
                $thisPath = $this.attr('src');

            $this.wrap('<a href="" target="_blank"></a>');
            $this.parent('a').attr('href', $thisPath);
        })
}

// ========================
// Helper, Validation Functions
// ========================
function getParameterByName(name, url) {
    if (!url)
        url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results)
        return null;
    if (!results[2])
        return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
function getTxtByLang(arrayTxt) {
    var currentLang = 0;
    switch (lang) {
        case 'zh-hk':
            currentLang = 1;
            break;
        case 'zh-cn':
            currentLang = 2;
            break;
        default:
            currentLang = 0;
    }
    return (arrayTxt[currentLang]);
}

function getMaxHeight($elem, mode) {
    var maxHeight = Math.max.apply(null, $elem.map(function () {
        if (mode == 'raw') {
            return $(this).height();
        } else if (mode == 'inner') {
            return $(this).innerHeight();
        } else {
            return $(this).outerHeight();
        }
    }).get());
    return maxHeight;
}
function getElemBottomPos($elem) {
    var bgTopPos = $elem.offset().top;
    var bgHeight = $elem.outerHeight();
    return (bgTopPos + bgHeight);
}
function setData($elem, data, val) {
    $elem.attr('data-' + data, val).data(data, val);
}
function unsetData($elem, data) {
    $elem.removeData(data).removeAttr('data-' + data);
}


function checkEnvironment() {
    if ($body.hasClass('chrome') && !$body.hasClass('edge')) {
        isChrome = true;
    } else if ($body.hasClass('firefox')) {
        isFirefox = true;
    } else if ($body.hasClass('safari')) {
        isSafari = true;
    } else if ($body.hasClass('edge')) {
        isEdge = true;
    } else if ($body.hasClass('trident')) {
        isIE = true;
    }

    if ((('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) && (!isSafari)) {
        $body.addClass('isMSTouchDevice');
        isMSTouchDevice = true;
    }
}

function initStatChart(){
  var $chart = $('.stat-chart');
  if(!$chart.length){
    return false;
  }
  
		var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    $chart.each(function(){
      var $thisChart = $(this);
      var $thisChartHolder = $thisChart.parent();
      var thisId = $thisChart.attr('id');
      
      var $thisDataTitle = $thisChartHolder.find('.stat-chart__title');
      var $thisXLabel = $thisChartHolder.find('.stat-chart__x-label');
      var $thisYLabel = $thisChartHolder.find('.stat-chart__y-label');
      var $thisDataLabel = $thisChartHolder.find('.stat-chart__data-label');
      var $thisDataScaleY = $thisChartHolder.find('.stat-chart__scale-y');
      var thisTitle = "";
      var thisXLabel = "";
      var thisYLabel = "";
      var thisDataLabel = "";
      
      var thisDataXLabelArr = [];
      var thisDataArr = [];
      var $thisDataSet = $thisChartHolder.find('.stat-chart__data');
      $thisDataSet.each(function(){
        var $thisData = $(this);
        var thisDataObj = {
            x: $thisData.data('x'),
            y: $thisData.data('y'),
        }
        var xLabel = $thisData.data('x-label');
        if(xLabel){
          thisDataXLabelArr.push(xLabel);
        }
        thisDataArr.push(thisDataObj);
      });
      
      
      if($thisDataTitle.length){
        thisTitle = $thisDataTitle.html();
      }
      if($thisXLabel.length){
        thisXLabel = $thisXLabel.html();
      }
      if($thisYLabel.length){
        thisYLabel = $thisYLabel.html();
      }
      if($thisDataLabel.length){
        thisDataLabel = $thisDataLabel.html();
      }
      
      var labels = false;
      if(thisDataXLabelArr.length>0){
          labels = thisDataXLabelArr;
      }
      
      var config = {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: thisDataLabel,
					backgroundColor: $thisDataLabel.data('color'),
					borderColor: $thisDataLabel.data('color'),
					data: thisDataArr,
					fill: false,
				}]
			},
			options: {
        elements:{
          line:{
                  tension: 0 // disables bezier curves
          }
        },
				responsive: true,
        aspectRatio: $(window).width() > 992 ? 2 : 1.3,
				title: {
					display: true,
					text: thisTitle
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: thisXLabel
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: thisYLabel
						}
					}]
				}
			}
		};
    
      if($thisDataScaleY.length){
          var scaleYMin = $thisDataScaleY.data('y-scale-min');
          var scaleYMax = $thisDataScaleY.data('y-scale-max');
          var scaleYStep = $thisDataScaleY.data('y-scale-step');
          
          var thisTicks = {};
          if(scaleYMin){
            thisTicks.min = scaleYMin;
          }
          if(scaleYMax){
            thisTicks.max = scaleYMax;
          }
          if(scaleYStep){
            thisTicks.stepSize = scaleYStep;
          }
          config['options']['scales']['yAxes'][0]['ticks'] = thisTicks;
      }
    
    var canvas = document.getElementById(thisId);
		var ctx = canvas.getContext('2d');
		window.myLine = new Chart(ctx, config);
    
    });
  
  

}
