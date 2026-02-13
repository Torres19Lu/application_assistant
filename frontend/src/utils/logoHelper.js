/**
 * 院校校徽辅助工具
 * 根据院校名称和国家生成彩色文字头像
 */

const COUNTRY_COLORS = {
  '美国': ['#1565C0', '#1976D2'],
  '英国': ['#C62828', '#D32F2F'],
  '新加坡': ['#AD1457', '#C2185B'],
  '中国香港': ['#E65100', '#EF6C00'],
  '澳大利亚': ['#2E7D32', '#388E3C'],
  '加拿大': ['#D84315', '#E64A19'],
  '瑞士': ['#6A1B9A', '#7B1FA2'],
  '日本': ['#00838F', '#0097A7'],
  '中国': ['#B71C1C', '#C62828'],
}

/**
 * 根据国家获取渐变色
 */
export function getUniColors(country) {
  return COUNTRY_COLORS[country] || ['#37474F', '#455A64']
}

/**
 * 根据国家获取单色
 */
export function getUniColor(country) {
  return getUniColors(country)[0]
}

/**
 * 获取院校名称首字
 */
export function getUniInitial(name) {
  return name ? name.charAt(0) : '?'
}

/**
 * 生成渐变样式
 */
export function getLogoGradient(country) {
  const [c1, c2] = getUniColors(country)
  return `linear-gradient(135deg, ${c1} 0%, ${c2} 100%)`
}
