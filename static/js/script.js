const app = new Vue({
  el: '#app',
  data() {
    return {
      budgetAmount: "",
      displayedBudget: 0,
      displayedExpense: 0,
      expenseName: "",
      expenseAmount: "",
      transactions: [],
      editMode: false,
      editIndex: null,
      modalActive: false,
    };
  },
  
  computed: {
    balance() {
      return (Number(this.displayedBudget) - this.expenses).toFixed(2);
    },
    
    expenses() {
      if (this.transactions.length === 0) return 0;
      let amounts = this.transactions.map(trans => parseFloat(trans.amount));
      return amounts.reduce((acc, cur) => acc + cur);
    },
    
    expenseTitle() {
      return (this.editMode) ? "Edit" : "Add An";
    },
    
    expenseSubmit() {
      return (this.editMode) ? "Update " : "Add";
    }
  },
  
  methods: {
    createBudget() {
      if (this.budgetAmount && Number(this.budgetAmount) > 0) {
        this.displayedBudget = Number(this.budgetAmount).toFixed(2);
        this.budgetAmount = "";
      }
    },
    
    formatAmount(e) {
      if (e.inputType === "insertFromPaste") {
        this.budgetAmount = parseFloat(this.budgetAmount).toFixed(2);
      }
      console.log(e);
    },
    
    onExpenseSubmit() {
      if (this.editMode) {
        this.transactions[this.editIndex].name = this.expenseName;
        this.transactions[this.editIndex].amount = this.expenseAmount;
        
        this.editMode = false;
      } else
      if (this.expenseName && this.expenseAmount && Number(this.expenseAmount) > 0) {
        let currentTransaction = {
          name: this.expenseName,
          amount: this.expenseAmount
        };
        
        this.transactions.push(currentTransaction);
      }
      this.expenseName = "";
      this.expenseAmount = "";
    },
    
    editTransaction(i) {
      this.editMode = true;
      this.editIndex = i;
      this.expenseName = this.transactions[i].name;
      this.expenseAmount = this.transactions[i].amount;
    },
    
    deleteTransaction() {
      this.transactions.splice(this.editIndex, 1);
      this.closeDeleteModal();
    },
    
    closeDeleteModal() {
      this.modalActive = false;
    },
    
    openDeleteModal(i) {
      this.modalActive = true;
      this.editIndex = i;
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const sidenav = document.getElementById("sidenav");
  const toggleSidebar = document.getElementById("toggleSidebar");

  let isOpen = true; // Initially open

  toggleSidebar.addEventListener("click", function () {
    isOpen = !isOpen;
    updateSidebarState();
  });

  function updateSidebarState() {
    sidenav.style.left = isOpen ? "0" : "-250px";
  }

  // Auto-hide sidebar on small screens
  const mediaQuery = window.matchMedia("(max-width: 600px)");

  function handleMediaQuery(event) {
    if (event.matches) {
      sidenav.style.left = "-250px";
      isOpen = false;
    } else {
      sidenav.style.left = "0";
      isOpen = true;
    }
  }

  handleMediaQuery(mediaQuery); // Initial check
  mediaQuery.addEventListener("change", handleMediaQuery); // Listen for changes
});