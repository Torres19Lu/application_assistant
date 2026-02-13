<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <div class="logo">
            <el-icon size="24" color="#1e40af"><School /></el-icon>
            <span>xmum留学</span>
          </div>
          <p class="description">
            为本科生提供全球硕士申请信息查询、院校专业对比、申请攻略等一站式服务
          </p>
        </div>
        
        <div class="footer-section">
          <h4>快速链接</h4>
          <ul>
            <li><router-link to="/universities">院校库</router-link></li>
            <li><router-link to="/majors">专业库</router-link></li>
            <li><router-link to="/guides">申请攻略</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>热门国家</h4>
          <ul>
            <li><a href="/universities?country=美国">美国</a></li>
            <li><a href="/universities?country=英国">英国</a></li>
            <li><a href="/universities?country=新加坡">新加坡</a></li>
            <li><a href="/universities?country=中国香港">中国香港</a></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>联系我们</h4>
          <ul>
            <li><el-icon><Message /></el-icon> contact@masterapp.com</li>
            <li><el-icon><Phone /></el-icon> 400-123-4567</li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>© 2026 xmum留学 版权所有</p>
        <div class="links">
          <a href="#">关于我们</a>
          <a href="#">隐私政策</a>
          <a href="#">使用条款</a>
          <a href="#">数据来源说明</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.footer {
  background: #1f2937;
  color: #9ca3af;
  padding: 60px 0 30px;
  margin-top: 80px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section {
  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    
    span {
      font-size: 18px;
      font-weight: 600;
      color: white;
    }
  }
  
  .description {
    font-size: 14px;
    line-height: 1.6;
  }
  
  h4 {
    color: white;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 20px;
  }
  
  ul {
    list-style: none;
    
    li {
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      
      a {
        color: #9ca3af;
        text-decoration: none;
        transition: color 0.3s;
        
        &:hover {
          color: white;
        }
      }
    }
  }
}

.footer-bottom {
  border-top: 1px solid #374151;
  padding-top: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  p {
    font-size: 14px;
  }
  
  .links {
    display: flex;
    gap: 24px;
    
    a {
      color: #9ca3af;
      text-decoration: none;
      font-size: 14px;
      transition: color 0.3s;
      
      &:hover {
        color: white;
      }
    }
  }
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
