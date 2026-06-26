<template>
    <UCard
        class="PostRenderer-MAIN w-full max-w-[75ch] mx-auto mb-6 bg-[var(--alexicon-surface)] text-[var(--alexicon-text)] shadow-[0_0_2ch_rgba(0,0,0,0.2)] border-0"
        :ui="{ root: 'border-0', header: 'border-0', body: 'border-0', footer: 'border-0' }"
		variant="ghost"
    >
        <template #header>
            <div class="flex items-center gap-3">
				<RouterLink :to="`/user/${postData.owner_id}`">
                	<UAvatar :src="authorAvatar" :alt="authorName" size="lg"/>
				</RouterLink>
                <div class="min-w-0">
                    <RouterLink :to="`/user/${postData.owner_id}`" class="font-semibold hover:underline">
                        {{ authorName }}
                    </RouterLink>

                    <div class="flex flex-wrap items-center gap-2 text-xs text-gray-400">
                        <RouterLink :to="`/post/${postData.id}`" class="hover:underline">
                            {{ formattedDate }}
                        </RouterLink>
                        <UBadge v-if="postData.ai_generated" color="neutral" variant="soft" class="ai-badge">
                            <UIcon name="i-lucide-bot" class="size-4"/> {{ $t('postRenderer.aiGenerated') }}
                        </UBadge>
                        <UBadge v-if="postData.nsfw_post" color="error" variant="soft">
                            NSFW
                        </UBadge>
                    </div>
                </div>
            </div>
        </template>

		<!-- content -->
        <div class="relative">
			<div :class="{ 'blur-md pointer-events-none select-none': isNsfwHidden }">
				<AlexiconMarkdown
					v-if="processedContent"
					:val="processedContent"
				/>
				<AlexiconMasonry
					v-if="multimedia.length"
					:media="multimedia"
					:cols-num="3"
				/>
				<AlexiconDoc
					v-for="file in files"
					:key="file.id"
					:file="file"
				/>
			</div>
			<div v-if="isNsfwHidden" class="absolute inset-0 backdrop-blur-md flex flex-col items-center justify-center gap-3">
				<UIcon name="i-lucide-triangle-alert" class="size-8 text-red-400"/>
				<p class="text-center text-sm" style="color: oklch(0.704 0.191 22.216); background-color: black;">
					&nbsp;{{ $t('postRenderer.thisPostContains') }}&nbsp;
				</p>
				<UButton color="error" @click="showNsfw = true">
					{{ $t('postRenderer.showContent') }}
				</UButton>
			</div>
		</div>

		<RouterLink
			v-if="postData.shared_post && !shared"
			:to="`/post/${postData.shared_post.id}`"
			class="shared-post-link"
		>
			<PostRenderer
				:post-data="postData.shared_post"
				:shared="true"
			/>
		</RouterLink>

		<!-- votes -->
        <template #footer>
            <div v-if="!shared" class="flex items-center justify-between border-t border-white/10 pt-3">
                <UButton icon="i-lucide-arrow-big-up" variant="ghost" :class="myVote === 'up' ? 'text-green-500' : ''" color="neutral" @click="vote('up')">
					{{ localVotes.up }}
				</UButton>

				<UButton icon="i-lucide-arrow-big-down" variant="ghost" :class="myVote === 'down' ? 'text-red-500' : ''" color="neutral" @click="vote('down')">
					{{ localVotes.down }}
				</UButton>

				<UButton icon="i-lucide-heart" variant="ghost" :class="myVote === 'heart' ? 'text-pink-500' : ''" color="neutral" @click="vote('heart')">
					{{ localVotes.heart }}
				</UButton>

                <UButton icon="i-lucide-message-circle" variant="ghost" color="neutral" @click="commentsOpen = !commentsOpen">
					{{ postData.comment_count || 0 }}
				</UButton>

				<UButton
					icon="i-lucide-forward"
					variant="ghost"
					color="neutral"
					@click="shareOpen = true"
				>
					{{ localSharesCount }}
				</UButton>

                <ContentOptionsMenu
					:entity-id="postData.id"
					entity-type="post"
					:owner-id="postData.owner_id"
					@deleted="$emit('deleted', postData.id)"
				/>
            </div>

			<!-- comment section -->
			<PostComments v-if="commentsOpen" :post-id="postData.id"/>
        </template>
    </UCard>

	<!-- sharing -->
	<UModal v-model:open="shareOpen" class="share-post-modal" :ui="{ content: 'max-w-[760px] w-[min(92vw,760px)] overflow-visible bg-transparent ring-0 shadow-none', overlay: 'bg-black/60 backdrop-blur-sm' }">
		<template #content>
			<UCard
				variant="ghost"
				class="w-full max-h-[85vh] overflow-y-auto bg-[var(--alexicon-surface)] text-[var(--alexicon-text)] shadow-[0_0_1ch_rgba(0,0,0,0.45)] border-0"
            	:ui="{ root: 'border-0', header: 'border-0', body: 'border-0', footer: 'border-0'}"
			>
				<template #header>
					<div class="flex items-center justify-between">
						<h2 class="font-bold">{{ $t('postRenderer.title') }}</h2>
						<UButton icon="i-lucide-x" variant="ghost" color="neutral" @click="shareOpen = false" />
					</div>
				</template>

				<UTextarea
					v-model="shareText"
					autoresize
					:rows="3"
					:placeholder="$t('postRenderer.placeholderContent')"
					:disabled="sharing"
					:ui="{ base: 'bg-black text-white placeholder:text-gray-500' }"
					class="w-full"
				/>

				<div class="mt-4 flex flex-wrap gap-4">
					<label class="flex items-center gap-2">
						<USwitch v-model="sharePrivate" /> {{ $t('postRenderer.private') }}
					</label>

					<label class="flex items-center gap-2">
						<USwitch v-model="shareNsfw" /> NSFW
					</label>

					<label class="flex items-center gap-2">
						<USwitch v-model="shareAiGenerated" /> {{ $t('postRenderer.aiGenerated') }}
					</label>
				</div>

				<template #footer>
					<div class="flex justify-end">
						<UButton class="w-full mt-2 items-center justify-center" color="primary" :loading="sharing" @click="sharePost">
							{{ $t('postRenderer.share') }}
						</UButton>
					</div>
				</template>
			</UCard>
		</template>
	</UModal>

</template>

<script>
const API_URL = import.meta.env.VITE_API_URL
import AlexiconMarkdown from '@/components/AlexiconMarkdown.vue'
import AlexiconMasonry from './AlexiconMasonry.vue'
import AlexiconDoc from './AlexiconDoc.vue'
import PostComments from './PostComments.vue'
import { putVote, deleteVote } from '@/services/yipnet/votes.js'
import { createPost } from '@/services/yipnet/posts'
import ContentOptionsMenu from './ContentOptionsMenu.vue'

export default {
    name: 'PostRenderer',
	emits: ['deleted'],
    components: {
        AlexiconMarkdown, AlexiconMasonry, AlexiconDoc, PostComments, ContentOptionsMenu,
    },
    props: {
		postData: {
			type: Object,
			default: () => ({})
		},

		shared: {
			type: Boolean,
			default: false
		}
    },
	data() {
		return {
			showNsfw: false,
			localVotes: {
				up: this.postData.votes?.up || 0,
				down: this.postData.votes?.down || 0,
				heart: this.postData.votes?.heart || 0
			},
			myVote: this.postData.viewer?.my_vote || null,
			commentsOpen: false,
			// share
			shareOpen: false,
			sharing: false,
			shareText: '',
			sharePrivate: false,
			shareNsfw: false,
			shareAiGenerated: false,
			localSharesCount: this.postData.shared_by_list?.length || 0,
		}
	},
	methods: {
		async vote(voteType) {
			try {
				const previousVote = this.myVote

				if (previousVote === voteType) {
					await deleteVote('post', this.postData.id)

					if (this.localVotes[voteType] > 0) {
						this.localVotes[voteType]--
					}

					this.myVote = null
					return
				}

				await putVote('post', this.postData.id, voteType)

				if (previousVote && this.localVotes[previousVote] > 0) {
					this.localVotes[previousVote]--
				}

				this.localVotes[voteType]++
				this.myVote = voteType
			} catch (error) {
				console.error(error)
			}
		},

		async sharePost() {
			if (this.sharing) return

			this.sharing = true

			try {
				const result = await createPost({
					content: this.shareText,
					media: [],
					sharing_id: this.postData.id,
					private_post: this.sharePrivate,
					nsfw_post: this.shareNsfw,
					ai_generated: this.shareAiGenerated
				})

				if (result.status === 'success') {
					this.shareOpen = false
					this.shareText = ''
					this.sharePrivate = false
					this.shareNsfw = false
					this.shareAiGenerated = false
					this.localSharesCount++
				}
			} finally {
				this.sharing = false
			}
		},

		getExtension(item) {
			const name = item.filename || item.name || item.url || ''
			return name.split('.').pop()?.toLowerCase() || ''
		},

		isMasonryMedia(item) {
			const ext = this.getExtension(item)

			const masonryImages = ['jpg', 'jpeg', 'png', 'gif', 'webp']
			const masonryVideos = ['mp4', 'mov', 'webm']

			return masonryImages.includes(ext) || masonryVideos.includes(ext)
		},
	},
    computed: {
		authorName() {
			return `${this.postData.name || ''} ${this.postData.surname || ''}`.trim()
		},

		authorAvatar() {
			if (!this.postData.profile_pic) return ''

			if (String(this.postData.profile_pic).startsWith('/')) {
				return `${API_URL}${this.postData.profile_pic}`
			}

			return `${API_URL}/alexicon/media/${this.postData.profile_pic}`
		},

		formattedDate() {
			if (!this.postData.post_date) return ''

			return new Date(this.postData.post_date).toLocaleString('es-MX', {
				dateStyle: 'medium',
				timeStyle: 'short'
			})
		},

		mediaWithUrl() {
			return (this.postData.media || []).map(item => ({
				...item,
				fullUrl: `${API_URL}${item.url}`
			}))
		},

		multimedia() {
			return this.mediaWithUrl.filter(item => this.isMasonryMedia(item))
		},

		files() {
			return this.mediaWithUrl.filter(item => !this.isMasonryMedia(item))
		},

		userSettings() {
			try {
				return JSON.parse(localStorage.getItem('alexicon_user') || '{}')
			} catch {
				return {}
			}
		},

		showNsfwSetting() {
			return !!this.userSettings.show_nsfw
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
			let text = String(this.postData.content || '')

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

		isNsfwHidden() {
			return this.postData.nsfw_post && !this.showNsfwSetting && !this.showNsfw
		}
	}
}
</script>

<style scoped lang="stylus">
.shared-post-link
    display block
    margin-top 1rem
    text-decoration none
    color inherit

.shared-post-link :deep(.PostRenderer-MAIN)
    max-width 100%
    margin-bottom 0
    border-left 8px solid rgba(128, 128, 128, 0.35)
</style>