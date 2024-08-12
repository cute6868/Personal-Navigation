// ------------------------------------------------------

// 1. 滚动到页面"顶部"后需要做的事情
function reachTop(btn) {
  btn.classList.remove('hide')  // 移除hide类，让按钮显示
}

// 2. 滚动到页面"底部"后需要做的事情
function reachBottom(btn) {
  btn.classList.remove('hide')  // 移除hide类，让按钮显示
}

// 3. 滚到页面的"其他区域"需要做的事情
function reachOther(btns) {
  btns.btnTop.classList.add('hide')     // 添加hide类，让按钮隐藏
  btns.btnBottom.classList.add('hide')  // 添加hide类，让按钮隐藏
}

// ------------------------------------------------------

// 1. 获取总共需要滚出去的距离
import { totalScroll } from "/utils/scroll.js";
const totalScrollTop = Math.round(totalScroll())

// 2. 获取上下两个按钮对象
const btnTop = document.querySelector('.btnTop')
const btnBottom = document.querySelector('.btnBottom')

// 3. 给"浏览器窗口"对象绑定事件监听
window.addEventListener('scroll', () => {

  // 3.1 获取当前滚出去了多少距离
  const currentScrollTop = Math.round(document.documentElement.scrollTop)

  // 3.2 根据滚轮位置，执行对应功能
  if (currentScrollTop === 0) { reachTop(btnTop) }  // 到达顶部
  else if (currentScrollTop === totalScrollTop) { reachBottom(btnBottom) }  // 到达底部
  else reachOther({   // 抵达其他区域
    btnTop: btnTop,
    btnBottom: btnBottom
  })
})

// ------------------------------------------------------

// 指定页面滚动到某个位置
function goTo(position) {
  window.scrollTo({
    top: position,
    behavior: 'smooth',
  })
}

// 给按钮添加事件监听
btnTop.addEventListener('click', () => {
  goTo(totalScrollTop)
})
btnBottom.addEventListener('click', ()=> {
  goTo(0)
})






