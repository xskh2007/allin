## 安装
git clone https://github.com/PanJiaChen/vue-admin-template.git
cd vue-admin-template
npm install
npm run dev

## 第一个页面  
依赖安装并成功启动后，接下来我们就开始我们的第一个页面的开发了。
在src/views下面创建我们Vue的展示页面。

- 1. 在src/views下面创建一个存放新页面的目录，例如是src/views/demo。
- 2. 在src/views/demo下创建index.vue。
- 3. 在src/router/index.js下创建对应的访问路由。
    
    src/views/demo/index.vue的内容如下：    
    
    
```    <!-- HTML -->
    <template>
      <div>
        <h1>Index</h1>
      </div>
    </template>
     
    <!-- Vue -->
    <script>
    export default {
      data() {
        return {
     
        }
      },
      methods: {
     
      }
    }
    </script>
     
    <!-- CSS样式 -->
    <style scoped>
     
    </style>
```    

    
 在src/router/index.js里面添加新页面对应的访问路由，添加注释的都是需要我们根据场景进行调整的：
 
     {
      path: '/demo',  // 访问的路由地址
      component: Layout,
      children: [{
        path: 'index', // 访问的路由地址
        name: 'DemoIndex', // 路由名称
        component: () => import('@/views/demo/index'), // 对应的展示页面地址，@表示src
        meta: { title: 'Demo', icon: 'dashboard' }  // title表示菜单展示的名称，icon表示图标
      }]
    }
    
    
到此一个简单的页面就创建完成了，通过 http://IP:Port/demo/index，就能访问到对应的页面信息了。

## Vue admin template配置登录

配置开发环境的跨域问题
修改.env.development文件

    VUE_APP_BASE_API = '/dev-api' 为 VUE_APP_BASE_API = ' ' 
    
在vue.config.js中的devServer里面加入以下内容：

    proxy: {
      // change xxx-api/login => mock/login
      // detail: https://cli.vuejs.org/config/#devserver-proxy
      [process.env.VUE_APP_BASE_API]: {
        // target: `http://127.0.0.1:${port}`,
        target: `http://localhost:8000`,
        changeOrigin: true,
        pathRewrite: {
          ['^' + process.env.VUE_APP_BASE_API]: ''
        }
      }
    }
    
注释mock，找到下面的代码，注释掉。

    // before: require('./mock/mock-server.js')
    
    
 调整API请求  
修改src/api/user.js为以下内容：   
    
    
    import request from '@/utils/request'

    export function login(data) {
      return request({
        url: '/api/v1.0.0/user/login',
        method: 'post',
        data
      })
    }
    
    export function getInfo(token) {
      return request({
        url: '/api/v1.0.0/user/userinfo',
        method: 'get'
      })
    }
    
    export function logout() {
      return request({
        url: '/vue-admin-template/user/logout',
        method: 'post'
      })
    }
    
    
    
 调整login函数  
vue admin template是的登录是使用vuex来处理的，我们需调整src/store/modules/user.js下的login动作。   

    // user login
    login({ commit }, userInfo) {
      const { username, password } = userInfo
      return new Promise((resolve, reject) => {
        login({ username: username.trim(), password: password }).then(response => {
          commit('SET_TOKEN', response.token)
          setToken(response.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
        
    
 设置身份验证Header参数  
在src/utils/requests.js文件中配置验证参数Authorization   
    
    
    config.headers['X-Token'] = getToken()
    将上面替换为如下：
    config.headers['Authorization'] = 'JWT ' + getToken()
        
    
修改请求状态码验证
    
    res.code !== 20000
    替换为：
    res.code !== 20000 && res.token === undefined
    
    
修改Login页面，移除测试相关数据  
文件位置：src/views/login/index.vue  
删除关于用户名和密码无意义的验证。  
删除自定义校验函数，搜索一下内容删除掉。  

    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    
    
    
删除自定义外部引入函数，搜索一下内容删除。  

    import { validUsername } from '@/utils/validate'


在rules中移除validUsername和validatePassword的触发函数。

    loginRules: {
      username: [{ required: true, trigger: 'blur', validator: validateUsername }],
      password: [{ required: true, trigger: 'blur', validator: validatePassword }]
    },
    替换为：
    loginRules: {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
    },


获取当前用户信息  
修改src/store/modules/user.js里面的getInfo函数。  


    // get user info
    getInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const { data } = response
     
          if (!data) {
            return reject('Verification failed, please Login again.')
          }
     
          const { username, avatar } = data
     
          commit('SET_NAME', username)
          commit('SET_AVATAR', avatar)
          resolve(data)
        }).catch(error => {
          reject(error)
        })
      })
    },
    
    
    
用户退出函数调整  
修改src/store/modules/user.js里面的logout函数。  

    
    // user logout
    logout({ commit, state }) {
      return new Promise((resolve, reject) => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      })
    }