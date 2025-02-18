document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const toggleButton = document.getElementById("toggle-sidebar");
//   const sidebarItems = document.getElementById("sidebar-items");
//   const newConnectButton = document.getElementById("new-connect");

  // Toggle sidebar collapse/expands
  toggleButton.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
  });

  // Handle sidebar link clicks
  function handleSidebarLinkClick(event) {
    event.preventDefault();
    const target = this.getAttribute("data-target");
    loadContent(target);
  }

  // Function to load content into main area
  function loadContent(target) {
    fetch(target)
      .then((response) => response.text())
      .then((html) => {
        document.getElementById("main-content").innerHTML = html;
      })
      .catch((error) => console.error("Error loading content:", error));
  }

//   // Add new item to sidebar
//   newConnectButton.addEventListener("click", function () {
//     const newItem = document.createElement("li");
//     const newLink = document.createElement("a");
//     const itemCount = sidebarItems.children.length + 1; // 用于生成唯一的标签和 URL

//     newLink.textContent = `New Connection ${itemCount}`;
//     newLink.href = "#";
//     newLink.setAttribute("data-target", `/new-connection-${itemCount}`); // 动态生成目标 URL

//     newLink.addEventListener("click", handleSidebarLinkClick); // 绑定点击事件
//     newItem.appendChild(newLink);
//     sidebarItems.appendChild(newItem);
//   });

  function addNewSidebarItem() {
    const sidebarItems = document.getElementById("sidebar-items");
    const newItem = document.createElement("li");
    const newLink = document.createElement("a");
    const itemCount = sidebarItems.children.length + 1; // 用于生成唯一的标签和 URL
  
    newLink.textContent = `New Connection ${itemCount}`;
    newLink.href = "#";
    newLink.setAttribute("data-target", `/new-connection-${itemCount}`); // 动态生成目标 URL
  
    // 为新链接添加点击事件监听器
    newLink.addEventListener("click", function(event) {
      event.preventDefault();
      const target = this.getAttribute("data-target");
      loadContent(target);
    });
  
    newItem.appendChild(newLink);
    sidebarItems.appendChild(newItem);
  }

  // Bind click events to existing sidebar items
  const sidebarLinks = document.querySelectorAll("#sidebar-items li a");
  sidebarLinks.forEach((link) => {
    link.addEventListener("click", handleSidebarLinkClick);
  });

  // 初始化弹窗和覆盖层
  document.getElementById("new-connect").addEventListener("click", function () {
    document.getElementById("connect-modal").style.display = "block";
    document.getElementById("connect-modal-overlay").style.display = "block";
  });

  // 关闭弹窗和覆盖层
  document
    .getElementById("connect-modal-overlay")
    .addEventListener("click", function () {
      document.getElementById("connect-modal").style.display = "none";
      document.getElementById("connect-modal-overlay").style.display = "none";
    });

  // 提交表单
  document
    .getElementById("connect-form")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 阻止默认表单提交

      var ip = document.getElementById("ip").value;
      var port = document.getElementById("port").value;
      var username = document.getElementById("username").value;
      var password = document.getElementById("password").value;

      var formData = new FormData();
      formData.append("ip", ip);
      formData.append("port", port);
      formData.append("username", username);
      formData.append("password", password);

      fetch("/add_connect", {
        // 假设你的路由是 /add_connect
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document.getElementById("connect-modal").style.display = "none";
            document.getElementById("connect-modal-overlay").style.display =
              "none";
            // 可以在这里刷新页面或更新UI
          } else {
            alert("Failed to add connection: " + data.error);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred while adding the connection.");
          addNewSidebarItem();
        });
    });
});
