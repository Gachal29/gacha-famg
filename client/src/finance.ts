import { createApp } from "vue";
import { FinanceController } from "./controller/finance-controller";
import Finance from "./components/Finance.vue";
import IconTrash from "./components/icons/IconTrash.vue";
import IconEdit from "./components/icons/IconEdit.vue";

const appId = "app-finance";

if (document.getElementById(appId)) {
  const controller = new FinanceController(
    window.requestContext.shops,
    window.requestContext.categories,
    window.requestContext.receipts,
    window.requestContext.purchase_items,
    window.innerWidth,
  );

  const app = createApp({
    data() {
      return {
        controller: controller,
      }
    }
  });

  app.component("finance", Finance);
  app.component("icon-trash", IconTrash);
  app.component("icon-edit", IconEdit);
  app.mount(`#${appId}`);
}
