/**
 * Created by chu on 17-12-18.
 */
$(function () {
    //加载完成，延迟开启，在jq初始化完成之后进行的，
    setTimeout(function () {
        //轮播开启，多个轮播，
        topSeiper();
        swiperMenu();
    }, 1000)


})

function topSeiper() {
    var topSwiper = new Swiper('#topSwiper', {
        loop: true,
        autoplay: 4000,
        // pagination:''
    })
}

function swiperMenu() {
    var topSwiper = new Swiper('#swiperMenu', {

        slidesPerView: 3,
        loop: true,
        autoplay: 4000,
    })
}
