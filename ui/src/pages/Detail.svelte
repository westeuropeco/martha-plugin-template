<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getPluginContext,
		type PluginRouteProps
	} from '@westeuropeco/martha-sdk/client';
	import Button from '@aiaiai/design-system/components/Button.svelte';
	import PageContainer from '@aiaiai-pt/design-system/components/PageContainer.svelte';
	import { ArrowLeft } from 'phosphor-svelte';
	import PageHeader from '@westeuropeco/admin-chrome/PageHeader.svelte';
	import { thingsApi } from '../api.js';
	import type { Thing } from '../types.js';

	const { params }: PluginRouteProps = $props();
	const ctx = getPluginContext();
	const api = thingsApi(ctx.api);

	let thing = $state<Thing | null>(null);
	let loading = $state(true);
	let loadError = $state('');

	onMount(async () => {
		try {
			thing = await api.get(params.id ?? '');
		} catch (e) {
			loadError = e instanceof Error ? e.message : 'Failed to load.';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>__PLUGIN_DISPLAY__ detail - Martha Admin</title>
</svelte:head>

<PageContainer>
	<PageHeader title={thing?.name ?? '__PLUGIN_DISPLAY__'} subtitle={thing?.description ?? ''}>
		{#snippet children()}
			<Button variant="ghost" onclick={() => ctx.navigation.goto('/plugins/__PLUGIN_SLUG__')}>
				{#snippet icon()}<ArrowLeft size={16} />{/snippet}
				Back
			</Button>
		{/snippet}
	</PageHeader>

	{#if loading}
		<div class="loading">Loading…</div>
	{:else if loadError}
		<div class="load-error" role="alert">{loadError}</div>
	{:else if thing}
		<dl class="kv">
			<dt>ID</dt>
			<dd>{thing.id}</dd>
			<dt>Name</dt>
			<dd>{thing.name}</dd>
			<dt>Description</dt>
			<dd>{thing.description || '—'}</dd>
		</dl>
	{/if}
</PageContainer>

<style>
	.loading {
		padding: var(--space-xl) 0;
		text-align: center;
		color: var(--color-text-secondary);
	}

	.load-error {
		padding: var(--space-md);
		border-radius: var(--radius-sm);
		background: var(--color-surface-raised);
		border: 1px solid var(--color-border);
		color: var(--color-error);
	}

	.kv {
		display: grid;
		grid-template-columns: max-content 1fr;
		gap: var(--space-sm) var(--space-lg);
		margin-top: var(--space-lg);
	}

	.kv dt {
		font-weight: 600;
		color: var(--color-text-secondary);
	}

	.kv dd {
		margin: 0;
	}
</style>
