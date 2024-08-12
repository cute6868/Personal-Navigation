// 计算"页面总共需要滚出去多少距离"才能抵达页面的底部
function totalScroll() {
  const docEle = document.documentElement   // 获取HTML元素对象
  const totalHeight = docEle.scrollHeight   // 获取页面内容的总高度
  const visualHeight = docEle.clientHeight  // 浏览器可视部分的高度
  return totalHeight - visualHeight         // 总共需要滚出去的距离
}

export {
  totalScroll
}