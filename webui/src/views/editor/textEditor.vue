<template>
  <div>
    <div style="border: 1px solid #ccc">
      <Toolbar
        :editor-id="editorId"
        :default-config="toolbarConfig"
        :mode="mode"
        style="border-bottom: 1px solid #ccc"
      />
      <Editor
        :editor-id="editorId"
        :default-config="editorConfig"
        :default-content="getDefaultContent"
        :default-html="defaultHtml"
        :mode="mode"
        style="height: 500px"
        @onCreated="handleCreated"
        @onChange="handleChange"
        @onDestroyed="handleDestroyed"
        @onFocus="handleFocus"
        @onBlur="handleBlur"
        @customAlert="customAlert"
        @customPaste="customPaste"
      />
    </div>
  </div>
</template>

<script>
import {
  defineComponent,
  computed,
  reactive,
  ref,
  toRefs,
  onBeforeUnmount
} from 'vue'
import {
  Editor,
  Toolbar,
  getEditor,
  removeEditor
} from '@wangeditor/editor-for-vue'

export default defineComponent({
  components: {
    Editor,
    Toolbar
  },
  setup() {
    const state = reactive({
      readOnly: false, //只读
      content: '<h1><strong>欢迎来到Admin-Frame-Vue3</strong></h1>'
    })

    const editorId = `w-e-${Math.random().toString().slice(-5)}` //【注意】编辑器 id ，要全局唯一

    // defaultContent (JSON 格式) 和 defaultHtml (HTML 格式) ，二选一
    const defaultHtml = '一行文字'
    const defaultContent = [
      // { type: 'paragraph', children: [{ text: '一行文字' }] }
    ]
    const getDefaultContent = computed(() =>
      JSON.parse(JSON.stringify(defaultContent))
    ) // 注意，要深拷贝 defaultContent ，否则报错

    const toolbarConfig = {}
    const editorConfig = { MENU_CONF: {}, placeholder: '请输入内容...' }
    editorConfig.MENU_CONF['uploadImage'] = {
      server: '/src/assets/image',
  

 
    //   // form-data fieldName ，默认值 'wangeditor-uploaded-image'
    //   fieldName: 'your-custom-name',

    //   // 单个文件的最大体积限制，默认为 2M
    //   maxFileSize: 1 * 1024 * 1024, // 1M

    //   // 最多可上传几个文件，默认为 100
    //   maxNumberOfFiles: 10,

    //   // 选择文件时的类型限制，默认为 ['image/*'] 。如不想限制，则设置为 []
      allowedFileTypes: ['image/*'],

    //   // 自定义上传参数，例如传递验证的 token 等。参数会被添加到 formData 中，一起上传到服务端。
    //   meta: {
    //     token: 'xxx',
    //     otherKey: 'yyy'
    //   },

    //   // 将 meta 拼接到 url 参数中，默认 false
    //   metaWithUrl: false,

    //   // 自定义增加 http  header
    //   headers: {
    //     Accept: 'text/x-json',
    //     otherKey: 'xxx'
    //   },

    //   // 跨域是否传递 cookie ，默认为 false
    //   withCredentials: true,

    //   // 超时时间，默认为 10 秒
    //   timeout: 5 * 1000, // 5 秒
    
 
    //   // 自定义插入图片
    //   customInsert(res, insertFn) {
    //     // res 即服务端的返回结果

    //     // 从 res 中找到 url alt href ，然后插图图片
    //     insertFn(res.url, res.alt, res.href)
    //   },

 
    //   // 自定义上传
    //   async customUpload(file, insertFn) {
    //     // file 即选中的文件
    //     // 自己实现上传，并得到图片 url alt href
    //     // 最后插入图片
    //     insertFn(file.url, file.alt, file.href)
    //   },
 
    //   // 自定义选择图片
    //   customBrowseAndUpload(insertFn) {
    //     // 自己选择文件
    //     // 自己上传文件，并得到图片 url alt href
    //     // 最后插入图片
    //     insertFn(insertFn.url, insertFn.alt, insertFn.href)
    //   },


    //   // 其他配置...

    //   // 小于该值就插入 base64 格式（而不上传），默认为 0
    //   base64LimitSize: 5 * 1024, // 5kb
    

    //   // 上传之前触发
    //   onBeforeUpload(files) {
    //     // files 选中的文件列表，格式如 { key1: file1, key2: file2 }
    //     return files

    //     // 返回值可选择：
    //     // 1. 返回一个对象（files 或者 files 的一部分），则将上传返回结果中的文件
    //     // 2. 返回 false ，终止上传
    //   },
    //   // 上传进度的回调函数
    //   onProgress(progress) {
    //     // progress 是 0-100 的数字
    //     console.log('progress', progress)
    //   },
    //   // 单个文件上传成功之后
    //   onSuccess(file, res) {
    //     console.log(`${file.name} 上传成功`, res)
    //   },
    //   // 单个文件上传失败
    //   onFailed(file, res) {
    //     console.log(`${file.name} 上传失败`, res)
    //   },
    //   // 上传错误，或者触发 timeout 超时
      onError(file, err, res) {
        console.log(`${file.name} 上传出错`, err, res)
      }
    }

    const handleCreated = (editor) => {
      console.log('created', editor)
    }
    const handleChange = (editor) => {
      console.log('change:', editor.children)
    }
    const handleDestroyed = (editor) => {
      console.log('destroyed', editor)
    }
    const handleFocus = (editor) => {
      console.log('focus', editor)
    }
    const handleBlur = (editor) => {
      console.log('blur', editor)
    }
    const customAlert = (info, type) => {
      alert(`【自定义提示】${type} - ${info}`)
    }
    const customPaste = (editor, event, callback) => {
      console.log('ClipboardEvent 粘贴事件对象', editor, event)

      // 自定义插入内容
      // editor.insertText('xxx')

      // 返回值（注意，vue 事件的返回值，不能用 return）
      callback(false) // 返回 false ，阻止默认粘贴行为
      // callback(true) // 返回 true ，继续默认的粘贴行为
    }
    // 组件销毁时，也及时销毁编辑器
    onBeforeUnmount(() => {
      const editor = getEditor(editorId)
      if (editor == null) return

      editor.destroy()
      removeEditor(editorId)
    })

    return {
      ...toRefs(state),
      editorId,
      mode: 'default',
      defaultHtml,
      getDefaultContent,
      toolbarConfig,
      editorConfig,
      handleCreated,
      handleChange,
      handleDestroyed,
      handleFocus,
      handleBlur,
      customAlert,
      customPaste
    }
  }
})
</script>
<style lang="scss" scoped></style>
