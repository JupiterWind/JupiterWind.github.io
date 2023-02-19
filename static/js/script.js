window.onload = function (){

    // 우클릭 방지
    document.oncontextmenu = function(){ return false; }
    
    window.addEventListener('scroll', handleScroll);

    // 랜덤 배경이미지 
    handleBgImage();
    
}

function handleBgImage() {
  let randomNumber = Math.floor(Math.random() * 15) + 1;
    document.querySelector('header img').setAttribute('src', 'static/img/bg0' + randomNumber + '.jpg');
  }

// 스크롤 애니메이션  
function handleScroll() {
    const elems = document.querySelectorAll('.up-on-scroll');
    elems.forEach(elem => {
      if (isElementUnderBottom(elem, -20)) {
        elem.style.opacity = "0";
        elem.style.transform = 'translateY(7rem)';
      } else {
        elem.style.opacity = "1";
        elem.style.transform = 'translateY(0px)';
      }
    })

    const elems_show = document.querySelectorAll('.show-on-scroll');
    elems_show.forEach(elem => {
      if (isElementInViewport(elem)) {
        elem.style.opacity = "1"; 
      } else {
        elem.style.opacity = "0";
      }
    })

    const elems_effect = document.querySelectorAll('.effect-on-scroll');
    elems_effect.forEach(elem => {
      if (isElementInViewport(elem)) {
        elem.classList.add('is_visible');
        elem.style.transform = ' scale(1)';
        elem.style.filter = 'blur(0rem)';
      } else {
        elem.classList.remove('is_visible');
        elem.style.transform = ' scale(2)';
        elem.style.filter = 'blur(1rem)';
      }
    })
}

// 화면이 보여지는지 확인하는 함수
function isElementUnderBottom(elem, triggerDiff) {
  const { top } = elem.getBoundingClientRect();
  const { innerHeight } = window;
  return top > innerHeight + (triggerDiff || 0);
}

// Helper function from: http://stackoverflow.com/a/7557433/274826
function isElementInViewport(el) {
  // special bonus for those using jQuery
  if (typeof jQuery === "function" && el instanceof jQuery) {
    el = el[0];
  }
  var rect = el.getBoundingClientRect();
  return (
    (rect.top <= 0
      && rect.bottom >= 0)
    ||
    (rect.bottom >= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.top <= (window.innerHeight || document.documentElement.clientHeight))
    ||
    (rect.top >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight))
  );
}
  
 
