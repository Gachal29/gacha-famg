<script setup lang="ts">
import type { FinanceController } from '../controller/finance-controller';
import { WINDOW_WIDTHS } from '../const/window-width-standard';

const props = defineProps(["controller"]);
const controller: FinanceController = props.controller;

type FormatedDate = {
  short: string
  long: string
}

const formatDate = (date: Date): FormatedDate => {
  const year = date.getFullYear();
  const month = date.getMonth()+1;
  const day = date.getDate();
  return {
    short: `${month}月${day}日`,
    long: `${year}年${month}月${day}日`,
  }
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="table table-xs lg:table-md">
      <thead class="text-center bg-accent-content text-neutral-content text-neutral-content">
        <tr>
          <th></th>
          <th>日付</th>
          <th>店</th>
          <th>カテゴリー</th>
          <th>詳細</th>
          <th>金額</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody
        class="border-b border-base-300"
        v-for="(receipt, idx) in controller.receipts" :key="idx"
      >
        <tr>
          <td class="text-center">{{ idx+1 }}</td>
          <td class="text-center whitespace-nowrap">
            <!-- 日付 -->
            <span
              class="tooltip"
              :data-tip="formatDate(receipt.date).long"
            >
              {{ formatDate(receipt.date).short }}
            </span>
          </td>
          <td class="text-center whitespace-nowrap">
            <!-- 店 -->
            <span
              :class="controller.getShop(receipt?.shopId) && 'badge text-xs lg:text-sm'"
              :style="controller.getShop(receipt?.shopId)?.badgeStyle"
            >
              {{ controller.getShop(receipt?.shopId)?.name ?? '' }}
            </span>
          </td>
        </tr>
        <tr
          class="border-0"
          v-for="(item, itemIdx) in receipt.purchaseItems" :key="itemIdx"
        >
          <!-- 購入品詳細 -->
          <td colspan="3"></td>
          <td class="text-center whitespace-nowrap">
            <!-- カテゴリー -->
            <span
              :class="controller.getCategory(item?.categoryId) && 'badge text-xs lg:text-sm'"
              :style="controller.getCategory(item?.categoryId)?.badgeStyle"
            >
              {{ controller.getCategory(item?.categoryId)?.name ?? '' }}
            </span>
          </td>
          <td class="whitespace-nowrap">
            <!-- 詳細 -->
            {{ item.detail }}
          </td>
          <td class="text-right">
            <!-- 金額 -->
            <span
              :class="item.discount && 'tooltip tooltip-primary text-primary whitespace-nowrap'"
              :data-tip="item.discount && `${item.discount.toLocaleString()}円割引`"
            >
              {{ item.priceTitle }}
            </span>
          </td>
          <td class="flex justify-center items-center">
            <!-- 操作ボタン -->
            <button class="mr-1 btn btn-success btn-xs btn-outline" title="編集">
              <icon-edit class="fill-success" />
              <span v-if="controller.innerWidth >= WINDOW_WIDTHS.xl">編集</span>
            </button>
            <button class="btn btn-error btn-xs btn-outline" title="削除">
              <icon-trash class="fill-error" />
              <span v-if="controller.innerWidth >= WINDOW_WIDTHS.xl">削除</span>
            </button>
          </td>
        </tr>
        <tr>
          <td colspan="5"></td>
          <td class="text-right font-bold whitespace-nowrap">小計：{{ receipt.totalPrice }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
