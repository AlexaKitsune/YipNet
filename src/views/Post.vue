<template>
    <YipNetLayout :user-data="userData" :on-session="onSession">
        <br/>
        
        <main class="mx-auto max-w-[75ch]">
            <div v-if="loading" class="p-6 opacity-70">
                Loading post...
            </div>

            <UAlert
                v-else-if="errorMessage"
                color="error"
                variant="soft"
                icon="i-lucide-triangle-alert"
                :title="errorMessage"
            />

            <PostRenderer
                v-else-if="postData.id"
                :post-data="postData"
                @deleted="goHome"
            />

            <p v-else class="p-6 text-center opacity-70">
                Post not found.
            </p>
        </main>
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import PostRenderer from '@/components/PostRenderer.vue'
import { getPost } from '@/services/yipnet/posts'

export default {
    name: 'Post',

    components: {
        YipNetLayout,
        PostRenderer
    },

    props: {
        userData: {
            type: Object,
            default: () => ({})
        },
        onSession: {
            type: Boolean,
            default: false
        }
    },

    data() {
        return {
            postData: {},
            loading: false,
            errorMessage: ''
        }
    },

    computed: {
        postId() {
            return Number(this.$route.params.id)
        }
    },

    methods: {
        async loadPost() {
            this.loading = true
            this.errorMessage = ''

            try {
                const result = await getPost(this.postId)
                this.postData = result.data || {}
            } catch (error) {
                this.errorMessage = error.message || 'No se pudo cargar el post.'
                this.postData = {}
            } finally {
                this.loading = false
            }
        },

        goHome() {
            this.$router.push('/')
        }
    },

    mounted() {
        this.loadPost()
    },

    watch: {
        '$route.params.id'() {
            this.loadPost()
        }
    }
}
</script>