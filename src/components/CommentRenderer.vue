<template>
    <div
        class="comment-node"
        :style="{ marginLeft: `${Math.min(depth, 4) * 1.25}rem` }"
    >
        <div class="rounded-lg bg-black/20 p-3">
            <div class="flex items-start gap-3">
                <UAvatar :src="authorAvatar(commentData)" :alt="authorName" size="md" />

                <div class="min-w-0 flex-1">
                    <div class="flex flex-wrap items-center gap-2">
                        <RouterLink :to="`/user/${commentData.owner_id}`" class="text-sm font-semibold hover:underline">
                            {{ authorName }}
                        </RouterLink>

                        <span class="text-xs text-gray-400">
                            {{ formatDate(commentData.comment_date) }}
                        </span>

                        <UBadge v-if="commentData.ai_generated" color="neutral" variant="soft" size="xs">
                            <UIcon name="i-lucide-bot" class="size-3" /> AI
                        </UBadge>
                    </div>

                    <div class="mt-2">
                        <AlexiconMarkdown :val="processedContent" />
                    </div>

                    <AlexiconMasonry
                        v-if="commentMultimedia(commentData).length"
                        :media="commentMultimedia(commentData)"
                        :cols-num="3"
                    />

                    <AlexiconDoc
                        v-for="file in commentFiles(commentData)"
                        :key="file.id"
                        :file="file"
                    />
                </div>
            </div>

            <div class="mt-3 flex items-center justify-between border-t border-white/10 pt-2">
                <div class="flex items-center gap-4">
                    <UButton icon="i-lucide-arrow-big-up" variant="ghost" color="neutral" :class="commentData.viewer?.my_vote === 'up' ? 'text-green-500' : ''" @click="voteComment('up')">
                        {{ commentData.votes?.up || 0 }}
                    </UButton>

                    <UButton icon="i-lucide-arrow-big-down" variant="ghost" color="neutral" :class="commentData.viewer?.my_vote === 'down' ? 'text-red-500' : ''" @click="voteComment('down')">
                        {{ commentData.votes?.down || 0 }}
                    </UButton>

                    <UButton icon="i-lucide-heart" variant="ghost" color="neutral" :class="commentData.viewer?.my_vote === 'heart' ? 'text-pink-500' : ''" @click="voteComment('heart')">
                        {{ commentData.votes?.heart || 0 }}
                    </UButton>
                </div>

                <div class="flex items-center gap-4">
                    <UButton icon="i-lucide-reply" variant="ghost" color="neutral" size="xs" @click="$emit('reply', commentData)">
                        {{ $t('commentRenderer.reply') }}
                    </UButton>

                    <ContentOptionsMenu
                        :entity-id="commentData.id"
                        entity-type="comment"
                        :owner-id="commentData.owner_id"
                        @deleted="$emit('deleted', $event)"
                    />
                </div>
            </div>
        </div>

        <div v-if="commentData.replies?.length" class="comment-replies">
            <CommentRenderer
                v-for="reply in commentData.replies"
                :key="reply.id"
                :comment-data="reply"
                :depth="depth + 1"
                @reply="$emit('reply', $event)"
                @deleted="$emit('deleted', $event)"
            />
        </div>
    </div>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import AlexiconMarkdown from '@/components/AlexiconMarkdown.vue'
import AlexiconMasonry from './AlexiconMasonry.vue'
import AlexiconDoc from './AlexiconDoc.vue'
import ContentOptionsMenu from './ContentOptionsMenu.vue'
import { putVote, deleteVote } from '@/services/yipnet/votes.js'

export default {
    name: 'CommentRenderer',

    emits: ['reply', 'deleted'],

    components: {
        AlexiconMarkdown,
        AlexiconMasonry,
        AlexiconDoc,
        ContentOptionsMenu
    },

    props: {
        commentData: {
            type: Object,
            default: () => ({})
        },

        depth: {
            type: Number,
            default: 0
        }
    },

    computed: {
        userSettings() {
            try {
                return JSON.parse(localStorage.getItem('alexicon_user') || '{}')
            } catch {
                return {}
            }
        },

        hideDeadnameSetting() {
            return !!this.userSettings.hide_deadname
        },

        replaceDeadnameSetting() {
            return !!this.userSettings.replace_deadname
        },

        deadname() {
            return String(this.userSettings.deadname || '').trim()
        },

        chosenName() {
            return String(this.userSettings.chosen_name || '').trim()
        },

        processedContent() {
            let text = String(this.commentData.content || '')

            if (!this.deadname) return text

            const escaped = this.deadname.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            const regex = new RegExp(`\\b${escaped}\\b`, 'gi')

            if (this.replaceDeadnameSetting && this.chosenName) {
                return text.replace(regex, this.chosenName)
            }

            if (this.hideDeadnameSetting) {
                return text.replace(regex, '[ hidden ]')
            }

            return text
        },

        authorName() {
            return `${this.commentData.name || ''} ${this.commentData.surname || ''}`.trim()
        }
    },

    methods: {
        formatDate(date) {
            if (!date) return ''

            return new Date(date).toLocaleString('es-MX', {
                dateStyle: 'medium',
                timeStyle: 'short'
            })
        },

        authorAvatar(comment) {
            if (!comment.profile_pic) return ''

            if (String(comment.profile_pic).startsWith('/')) {
                return `${API_URL}${comment.profile_pic}`
            }

            return `${API_URL}/alexicon/media/${comment.profile_pic}`
        },

        commentMediaWithUrl(comment) {
            let media = comment.media || []

            if (typeof media === 'string') {
                try {
                    media = JSON.parse(media)
                } catch {
                    media = []
                }
            }

            if (!Array.isArray(media)) {
                media = []
            }

            return media.map(item => ({
                ...item,
                fullUrl: `${API_URL}${item.url}`
            }))
        },

        commentMultimedia(comment) {
            return this.commentMediaWithUrl(comment).filter(item =>
                this.isMasonryMedia(item)
            )
        },

        commentFiles(comment) {
            return this.commentMediaWithUrl(comment).filter(item =>
                !this.isMasonryMedia(item)
            )
        },

        async voteComment(voteType) {
            const comment = this.commentData
            const previousVote = comment.viewer?.my_vote || null

            if (!comment.votes) {
                comment.votes = {
                    up: 0,
                    down: 0,
                    heart: 0
                }
            }

            if (!comment.viewer) {
                comment.viewer = {
                    my_vote: null
                }
            }

            if (previousVote === voteType) {
                await deleteVote('comment', comment.id)

                if (comment.votes[voteType] > 0) {
                    comment.votes[voteType]--
                }

                comment.viewer.my_vote = null
                return
            }

            await putVote('comment', comment.id, voteType)

            if (previousVote && comment.votes[previousVote] > 0) {
                comment.votes[previousVote]--
            }

            comment.votes[voteType]++
            comment.viewer.my_vote = voteType
        },

        getExtension(item) {
            const name = item?.filename || item?.name || item?.url || ''
            return name.includes('.')
                ? name.split('.').pop().toLowerCase()
                : ''
        },

        isMasonryMedia(item) {
            const ext = this.getExtension(item)

            const masonryImages = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            const masonryVideos = ['mp4', 'mov', 'webm']

            return masonryImages.includes(ext) || masonryVideos.includes(ext)
        },
    }
}
</script>

<style scoped lang="stylus">
.comment-node
    position relative
    margin-top 0.75rem

.comment-node::before
    content ''
    position absolute
    left -0.65rem
    top 0
    bottom 0
    width 2px
    background rgba(255, 255, 255, 0.08)

.comment-replies
    margin-top 0.75rem
</style>