<template>
	<YipNetLayout :user-data="userData" :on-session="onSession">
        
        <br/>
		<UCard class="bg-[var(--alexicon-surface)] border-0" variant="ghost">
			<template #header>
				<h1 class="text-xl font-bold">Statistics</h1>
				<p class="text-sm opacity-70">
					{{ entityType }} #{{ entityId }}
				</p>
			</template>

			<div v-if="loading">Loading...</div>

			<div v-else-if="stats" class="space-y-6">
				<div class="grid grid-cols-2 md:grid-cols-4 gap-3">
					<UCard v-for="item in summaryCards" :key="item.label" class="bg-black/20 border-0" variant="ghost">
						<p class="text-sm opacity-70">{{ item.label }}</p>
						<p class="text-2xl font-bold">{{ item.value }}</p>
					</UCard>
				</div>
                
                <UCard class="bg-black/20 border-0" variant="ghost">
                    <h2 class="font-semibold mb-4">
                        Votes per comment
                    </h2>

                    <div class="ratio-tracker">
                        <div
                            class="ratio-tracker-fill"
                            :style="{
                                width: `${Math.min(Number(summary.vote_comment_ratio || 0) * 100, 100)}%`
                            }"
                        />
                    </div>

                    <div class="mt-2 flex justify-between text-sm opacity-70">
                        <span>{{ summary.vote_comment_ratio || 0 }}</span>
                        <span>
                            {{
                                Number(summary.vote_comment_ratio || 0) >= 2
                                    ? 'High'
                                    : Number(summary.vote_comment_ratio || 0) >= 1
                                        ? 'Good'
                                        : 'Low'
                            }}
                        </span>
                    </div>

                    <p class="mt-2 text-xs opacity-50">
                        {{ summary.votes || 0 }} votes / {{ summary.comments || 0 }} comments
                    </p>
                </UCard>

				<UCard class="bg-black/20 border-0" variant="ghost">
					<h2 class="font-semibold mb-4">Views by day</h2>
					<LineChart
                        v-if="dailyViewsChart.length"
                        :data="dailyViewsChart"
                        x-axis="date"
                        :y-axis="['views']"
                        :categories="{
                            views: {
                                name: 'Views'
                            }
                        }"
                    />
                    <p v-else class="text-sm opacity-60">
                        No views yet.
                    </p>
				</UCard>

                <UCard class="bg-black/20 border-0" variant="ghost">
                    <h2 class="font-semibold mb-4">Votes by day</h2>

                    <LineChart
                        v-if="dailyVotesChart.length"
                        :data="dailyVotesChart"
                        x-axis="date"
                        :y-axis="['heart', 'up', 'down', 'score']"
                        :categories="{
                            heart: { name: 'Hearts', color: '#ec4899' },
                            up: { name: 'Upvotes', color: '#22c55e' },
                            down: { name: 'Downvotes', color: '#ef4444' },
                            score: { name: 'Score', color: '#7700ff' }
                        }"
                    />
                    <p v-else class="text-sm opacity-60">
                        No votes by day yet.
                    </p>
                </UCard>

				<UCard class="bg-black/20 border-0" variant="ghost">
					<h2 class="font-semibold mb-4">Vote distribution</h2>
					<BarChart
                        v-if="votesChart.length"
                        :data="votesChart"
                        x-axis="type"
                        :y-axis="['heart', 'up', 'down']"
                        :categories="{
                            heart: {
                                name: 'Hearts',
                                color: '#ec4899'
                            },
                            up: {
                                name: 'Upvotes',
                                color: '#22c55e'
                            },
                            down: {
                                name: 'Downvotes',
                                color: '#ef4444'
                            }
                        }"
                    />
                    <p v-else class="text-sm opacity-60">
                        No votes yet.
                    </p>
				</UCard>

                <UCard class="bg-black/20 border-0" variant="ghost">
                    <h2 class="font-semibold mb-4">Voters</h2>

                    <div class="grid grid-cols-3 gap-2 rounded-md bg-transparent mb-4">
                        <button class="stats-tab" :class="{ 'stats-tab-active': activeVoteTab === 'heart' }" @click="activeVoteTab = 'heart'">
                            <UIcon name="i-lucide-heart" /> Hearts
                        </button>

                        <button class="stats-tab" :class="{ 'stats-tab-active': activeVoteTab === 'up' }" @click="activeVoteTab = 'up'">
                            <UIcon name="i-lucide-arrow-up" /> Up
                        </button>

                        <button class="stats-tab" :class="{ 'stats-tab-active': activeVoteTab === 'down' }" @click="activeVoteTab = 'down'">
                            <UIcon name="i-lucide-arrow-down" /> Down
                        </button>
                    </div>

                    <div v-if="activeVoters.length" class="space-y-2">
                        <RouterLink
                            v-for="user in activeVoters"
                            :key="user.id"
                            :to="`/user/${user.id}`"
                            class="voter-row"
                        >
                            <UAvatar :src="userAvatar(user.profile_pic)" />

                            <div>
                                <p class="font-semibold">
                                    {{ user.name }} {{ user.surname }}
                                </p>
                                <p class="text-xs opacity-60">
                                    @{{ user.at_sign || user.nickname }}
                                </p>
                            </div>
                        </RouterLink>
                    </div>

                    <p v-else class="text-sm opacity-60">
                        No voters yet.
                    </p>
                </UCard>

			</div>
		</UCard>

        <br/>
	</YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import { getStats } from '@/services/yipnet/stats'
import { LineChart, BarChart } from 'vue-chrts'

export default {
	name: 'Stats',

	components: {
		YipNetLayout,
		LineChart,
		BarChart
	},

	data() {
		return {
			loading: false,
			stats: null,
            activeVoteTab: 'heart',
		}
	},

	computed: {
		entityId() {
			return Number(this.$route.params.id)
		},

		entityType() {
			return this.$route.query.type || this.$route.params.type
		},

		summary() {
			return this.stats?.summary || {}
		},

		summaryCards() {
			return [
				{ label: 'Views', value: this.summary.views || 0 },
				{ label: 'Votes', value: this.summary.votes || 0 },
				{ label: 'Hearts', value: this.summary.hearts || 0 },
				{ label: 'Score', value: (this.summary.ups || 0) - (this.summary.downs || 0) },
                //{ label: 'Vote/comment ratio', value: this.summary.vote_comment_ratio || 0 }
			]
		},

		dailyViewsChart() {
            const rows = this.stats?.daily_views || []

            return rows.map(item => ({
                date: String(item.date),
                views: Number(item.count || 0)
            }))
        },

        votesChart() {
            return [
                {
                    type: 'Heart',
                    heart: Number(this.summary.hearts || 0),
                    up: 0,
                    down: 0
                },
                {
                    type: 'Up',
                    heart: 0,
                    up: Number(this.summary.ups || 0),
                    down: 0
                },
                {
                    type: 'Down',
                    heart: 0,
                    up: 0,
                    down: Number(this.summary.downs || 0)
                }
            ]
        },

        dailyVotesChart() {
            const rows = this.stats?.daily_votes || []

            return rows.map(item => {
                const heart = Number(item.heart || 0)
                const up = Number(item.up || 0)
                const down = Number(item.down || 0)

                return {
                    date: String(item.date),
                    heart,
                    up,
                    down,
                    score: up - down
                }
            })
        },

        voters() {
            return this.stats?.voters || {
                heart: [],
                up: [],
                down: []
            }
        },

        activeVoters() {
            return this.voters[this.activeVoteTab] || []
        }
	},

	methods: {
		async loadStats() {
			this.loading = true

			try {
				const result = await getStats(this.entityType, this.entityId)
				this.stats = result.data
			} finally {
				this.loading = false
			}
		},

        userAvatar(value) {
            if (!value) return ''
            if (String(value).startsWith('/')) return `${import.meta.env.VITE_API_URL}${value}`
            return `${import.meta.env.VITE_API_URL}/alexicon/media/${value}`
        }
	},

	mounted() {
		this.loadStats()
	}
}
</script>

<style scoped lang="stylus">
.stats-tab
    display flex
    align-items center
    justify-content center
    gap 0.5ch
    padding 0.75ch 1ch
    border-radius 6px
    color #9ca3af
    background transparent
    transition all 0.15s

    &:hover
        background #3a3a3a
        color white

.stats-tab-active
    background #3a3a3a
    color white

.voter-row
    display flex
    align-items center
    gap 0.75rem
    padding 0.75rem
    border-radius 10px
    background rgba(0, 0, 0, 0.18)
    color inherit
    text-decoration none

    &:hover
        background #3a3a3a

/* ratio */
.ratio-tracker
    width 100%
    height 16px
    border-radius 999px
    overflow hidden
    background rgba(255,255,255,0.08)

.ratio-tracker-fill
    height 100%
    border-radius inherit
    background linear-gradient(
        90deg,
        #7700ff,
        #9f4dff
    )
    transition width .25s ease
</style>