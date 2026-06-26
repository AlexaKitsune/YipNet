<template>
    <YipNetLayout :user-data="userData" :on-session="onSession">
        <main
            ref="feedScroller"
            class="feed-scroll"
            @touchstart.passive="onPullStart"
            @touchmove.passive="onPullMove"
            @touchend="onPullEnd"
        >
            <div class="pull-refresh" :style="{ height: `${pullDistance}px` }">
                <UIcon
                    v-if="pullDistance >= pullThreshold"
                    :name="refreshing ? 'i-lucide-loader-circle' : 'i-lucide-arrow-down'"
                    :class="{ 'animate-spin': refreshing }"
                />

                <span v-if="refreshing">{{ $t('feed.refreshing') }}</span>
                <span v-else-if="pullDistance >= pullThreshold">{{ $t('feed.release') }}</span>
            </div>
            <br/>

            <PostRenderer
                v-for="post in posts"
                :key="post.id"
                :post-data="post"
            />
        </main>

        <div
            v-if="!postCreatorActive"
            class="YipNet-toggle-post-creator"
            @click="postCreatorActive = true"
        >
            <UIcon name="i-lucide-square-pen" class="size-6 text-white" />
        </div>

        <PostCreator
            v-else
            @close="postCreatorActive = false"
            @update-post="handlePostCreated"
        />
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue';
import PostCreator from '@/components/PostCreator.vue';
import { getFeed } from '@/services/yipnet/posts';
import PostRenderer from '@/components/PostRenderer.vue';

export default {
	name: 'Feed',
	components: {
		YipNetLayout, PostCreator, PostRenderer,
	},
	data() {
        return {
            posts: [],
            loading: false,
            errorMessage: '',
            postCreatorActive: false,

            refreshing: false,
            pulling: false,
            startY: 0,
            pullDistance: 0,
            pullThreshold: 80
        }
    },
	methods: {
        onPullStart(event) {
            const scroller = this.$refs.feedScroller

            if (!scroller || scroller.scrollTop > 0 || this.refreshing) {
                return
            }

            this.pulling = true
            this.startY = event.touches[0].clientY
        },

        onPullMove(event) {
            if (!this.pulling || this.refreshing) return

            const currentY = event.touches[0].clientY
            const distance = currentY - this.startY

            if (distance > 0) {
                this.pullDistance = Math.min(distance * 0.45, 120)
            }
        },

        async onPullEnd() {
            if (!this.pulling) return

            this.pulling = false

            if (this.pullDistance >= this.pullThreshold) {
                await this.refreshFeed()
            }

            this.pullDistance = 0
        },

        async refreshFeed() {
            if (this.refreshing) return

            this.refreshing = true

            try {
                await this.loadFeed()
            } finally {
                this.refreshing = false
            }
        },

        async loadFeed() {
            this.loading = true;
            this.errorMessage = '';
            try {
                const result = await getFeed()
                this.posts = result.data.posts || []
            } catch (error) {
                this.errorMessage = error.message || 'No se pudo cargar el feed.';
            } finally {
                this.loading = false;
            }
        },

        async handlePostCreated() {
            this.postCreatorActive = false
            await this.loadFeed()
        },
    },
	mounted() {
        this.loadFeed();
    }
}
</script>

<style scoped lang="stylus">
.YipNet-toggle-post-creator
    background-color: #7701ff
    position: fixed
    width: 50px
    aspect-ratio: 1/1
    right: 15px
    bottom: 15px
    border-radius: 100vw
    display: flex
    flex-direction: column
    align-items: center
    justify-content: center
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.25)
    z-index: 1

    &:hover
        cursor: pointer
        scale: 1.1
        transition: all 0.1s

.pull-refresh
    width 100%
    max-width 760px
    margin 0 auto
    display flex
    flex-direction column
    align-items center
    justify-content center
    text-align center
</style>