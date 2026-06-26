<template>
    <section
        class="MessageRenderer-MAIN"
        :class="isMine ? 'side-right' : 'side-left'"
        :id="`MessageRenderer-${messageData.id}`"
    >
        <div class="message-meta" v-if="!isMine">
            <UAvatar
                :src="avatarUrl(messageData.profile_pic)"
                :alt="senderName"
                size="xs"
            />

            <span>{{ senderName }}</span>
        </div>

        <div class="msg-bubble">
            <AlexiconMarkdown
                v-if="messageData.content"
                :val="messageData.content"
            />

            <AlexiconMasonry
                v-if="multimedia.length"
                :media="multimedia"
                :cols-num="2"
                class="mt-2"
            />

            <AlexiconDoc
                v-for="file in files"
                :key="file.id"
                :file="file"
                class="mt-2"
            />

            <!-- votes -->
            <div class="message-votes">
                <UButton
                    icon="i-lucide-arrow-big-up"
                    variant="ghost"
                    color="neutral"
                    size="xs"
                    :class="myVote === 'up' ? 'text-green-500' : ''"
                    @click="vote('up')"
                >
                    {{ localVotes.up }}
                </UButton>

                <UButton
                    icon="i-lucide-arrow-big-down"
                    variant="ghost"
                    color="neutral"
                    size="xs"
                    :class="myVote === 'down' ? 'text-red-500' : ''"
                    @click="vote('down')"
                >
                    {{ localVotes.down }}
                </UButton>

                <UButton
                    icon="i-lucide-heart"
                    variant="ghost"
                    color="neutral"
                    size="xs"
                    :class="myVote === 'heart' ? 'text-pink-500' : ''"
                    @click="vote('heart')"
                >
                    {{ localVotes.heart }}
                </UButton>

                <ContentOptionsMenu
                    :entity-id="messageData.id"
                    entity-type="message"
                    :owner-id="messageData.sender_id"
                    @reported="reportedMessage"
                />
            </div>

            <p class="mt-1 text-[11px] opacity-50">
                {{ formattedDate }}
            </p>
        </div>
    </section>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import AlexiconMarkdown from '@/components/AlexiconMarkdown.vue'
import AlexiconMasonry from '@/components/AlexiconMasonry.vue'
import AlexiconDoc from '@/components/AlexiconDoc.vue'
import ContentOptionsMenu from '@/components/ContentOptionsMenu.vue'
import { putVote, deleteVote } from '@/services/yipnet/votes.js'

export default {
    name: 'MessageRenderer',
    components: {
        AlexiconMarkdown,
        AlexiconMasonry,
        AlexiconDoc,
        ContentOptionsMenu,
    },
    props: {
        currentUserId: {
            type: Number,
            default: null
        },

        messageData: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            localVotes: {
                up: this.messageData.votes?.up || 0,
                down: this.messageData.votes?.down || 0,
                heart: this.messageData.votes?.heart || 0
            },
            myVote: this.messageData.viewer?.my_vote || null
        }
    },
    computed: {
        isMine() {
            return Number(this.messageData.sender_id) === Number(this.currentUserId)
        },

        senderName() {
            return `${this.messageData.name || ''} ${this.messageData.surname || ''}`.trim()
        },

        formattedDate() {
            if (!this.messageData.msg_date) return ''

            return new Date(this.messageData.msg_date).toLocaleString('es-MX', {
                dateStyle: 'short',
                timeStyle: 'short'
            })
        },

        mediaWithUrl() {
            let media = this.messageData.media || []

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

            return media.map(item => {
                if (typeof item === 'number') {
                    return {
                        id: item,
                        url: `/alexicon/media/${item}`,
                        fullUrl: `${API_URL}/alexicon/media/${item}`,
                        type: ''
                    }
                }

                return {
                    ...item,
                    fullUrl: item.url?.startsWith('http')
                        ? item.url
                        : `${API_URL}${item.url}`
                }
            })
        },

        multimedia() {
            return this.mediaWithUrl.filter(item => this.isMasonryMedia(item))
        },

        files() {
            return this.mediaWithUrl.filter(item => !this.isMasonryMedia(item))
        },
    },

    methods: {
        avatarUrl(value) {
            if (!value) return ''
            if (String(value).startsWith('/')) 
                return `${API_URL}${value}`
            return `${API_URL}/alexicon/media/${value}`
        },

        async vote(voteType) {
            try {
                const previousVote = this.myVote

                if (previousVote === voteType) {
                    await deleteVote('message', this.messageData.id)

                    if (this.localVotes[voteType] > 0) {
                        this.localVotes[voteType]--
                    }

                    this.myVote = null
                    return
                }

                await putVote('message', this.messageData.id, voteType)

                if (previousVote && this.localVotes[previousVote] > 0) {
                    this.localVotes[previousVote]--
                }

                this.localVotes[voteType]++
                this.myVote = voteType
            } catch (error) {
                console.error(error)
            }
        },

        reportedMessage() {
            console.log('Message reported')
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
.MessageRenderer-MAIN
    width 100%
    display flex
    flex-direction column
    margin-bottom 0.75rem

.side-left
    align-items flex-start

.side-right
    align-items flex-end

.message-meta
    display flex
    align-items center
    gap 0.5rem
    margin-bottom 0.25rem
    font-size 0.75rem
    opacity 0.65

.msg-bubble
    width fit-content
    max-width min(75%, 680px)
    padding 0.75rem
    border-radius 14px
    overflow hidden

.side-right .msg-bubble
    background #7700ff
    color white
    border-bottom-right-radius 4px

.side-left .msg-bubble
    background rgba(0, 0, 0, 0.22)
    color inherit
    border-bottom-left-radius 4px

.msg-bubble :deep(p:first-child)
    margin-top 0

.msg-bubble :deep(p:last-child)
    margin-bottom 0

/* votes */
.message-votes
    display flex
    align-items center
    gap 0.25rem
    margin-top 0.5rem
    opacity 0.85

.side-right .message-votes :deep(button)
    color white
</style>