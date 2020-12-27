<template>
  <div ref="tool" class="flow-menu">
    <div v-for="menu in menuList" :key="menu.id">
      <span class="ef-node-pmenu" @click="menu.open = !menu.open"><i
        :class="{'el-icon-caret-bottom': menu.open,'el-icon-caret-right': !menu.open}"
      />&nbsp;{{ menu.name }}</span>
      <ul v-show="menu.open" class="ef-node-menu-ul">
        <draggable v-model="menu.children" :options="draggableOptions" @end="end" @start="move">
          <li v-for="subMenu in menu.children" :key="subMenu.id" :type="subMenu.id" class="ef-node-menu-li">
            <i :class="subMenu.ico" /> {{ subMenu.name }}
          </li>
        </draggable>
      </ul>
    </div>
  </div>
</template>
<script>
import draggable from 'vuedraggable'

var mousePosition = {
  left: -1,
  top: -1
}

export default {
  components: {
    draggable
  },
  data() {
    return {
      activeNames: '1',
      // draggable配置参数参考 https://www.cnblogs.com/weixin186/p/10108679.html
      draggableOptions: {
        preventOnFilter: false,
        sort: false,
        disabled: false,
        ghostClass: 'tt',
        // 不使用H5原生的配置
        forceFallback: true
        // 拖拽的时候样式
        // fallbackClass: 'flow-node-draggable'
      },
      // 默认打开的左侧菜单的id
      defaultOpeneds: ['1', '2'],
      menuList: [
        {
          id: '1',
          type: 'group',
          name: '数据源',
          ico: 'el-icon-video-play',
          open: true,
          children: [
            {
              id: '11',
              type: 'timer',
              name: '数据接入',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '12',
              type: 'task',
              name: '接口调用',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '13',
              type: 'task',
              name: '数据库',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '14',
              type: 'task',
              name: '文件服务器',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '15',
              type: 'task',
              name: '大数据平台',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '16',
              type: 'task',
              name: '服务接口',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '17',
              type: 'task',
              name: '消息队列',
              ico: 'el-icon-odometer',
              // 自定义覆盖样式
              style: {}
            }
          ]
        },
        {
          id: '2',
          type: 'group',
          name: '转换',
          ico: 'el-icon-video-play',
          open: true,
          children: [
            {
              id: '21',
              type: 'clear',
              name: '数据清洗',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '22',
              type: 'clear',
              name: '基于函数转换',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '23',
              type: 'clear',
              name: '修改列明',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '24',
              type: 'clear',
              name: '缺失值填充',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '25',
              type: 'clear',
              name: '去除重复行',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '26',
              type: 'clear',
              name: '按比例采样',
              ico: 'el-icon-time',
              // 自定义覆盖样式
              style: {}
            }
          ]
        },
        {
          id: '3',
          type: 'group',
          name: '目标数据库',
          ico: 'el-icon-video-pause',
          open: true,
          children: [
            {
              id: '31',
              type: 'end',
              name: '流程结束',
              ico: 'el-icon-caret-right',
              // 自定义覆盖样式
              style: {}
            }, {
              id: '32',
              type: 'over',
              name: '数据结束',
              ico: 'el-icon-shopping-cart-full',
              // 自定义覆盖样式
              style: {}
            }
          ]
        }
      ],
      nodeMenu: {}
    }
  },
  created() {
    /**
       * 以下是为了解决在火狐浏览器上推拽时弹出tab页到搜索问题
       * @param event
       */
    if (this.isFirefox()) {
      document.body.ondrop = function(event) {
        // 解决火狐浏览器无法获取鼠标拖拽结束的坐标问题
        mousePosition.left = event.layerX
        mousePosition.top = event.clientY - 50
        event.preventDefault()
        event.stopPropagation()
      }
    }
  },
  methods: {
    // 根据id获取左侧菜单对象
    getMenuByType(id) {
      for (let i = 0; i < this.menuList.length; i++) {
        const children = this.menuList[i].children
        for (let j = 0; j < children.length; j++) {
          if (children[j].id === id) {
            return children[j]
          }
        }
      }
    },
    // 拖拽开始时触发
    move(evt, a, b, c) {
      var id = evt.item.attributes.type.nodeValue
      this.nodeMenu = this.getMenuByType(id)
    },
    // 拖拽结束时触发
    end(evt, e) {
      console.log('放置的节点，还没有连接')
      this.$emit('addNode', evt, this.nodeMenu, mousePosition)
    },
    // 是否是火狐浏览器
    isFirefox() {
      var userAgent = navigator.userAgent
      if (userAgent.indexOf('Firefox') > -1) {
        return true
      }
      return false
    }
  }
}
</script>
