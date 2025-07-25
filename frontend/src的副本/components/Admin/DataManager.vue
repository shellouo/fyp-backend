<template>
  <div>
    <div class="panel-header">
      <h3>User Management</h3>
      <div style="display:flex; gap:12px;">
        <el-input v-model="search" size="small" placeholder="Search users..." style="width:180px;" clearable />
        <el-button type="primary" size="small" @click="addUser">+ Add User</el-button>
      </div>
    </div>
    <el-table :data="pagedUsers" border stripe class="user-table">
      <el-table-column prop="username" label="Username" width="140" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="membership" label="Membership" width="120">
        <template #default="scope">
          <el-tag :type="tagType(scope.row.membership)">
            {{scope.row.membership}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="Status" width="90">
        <template #default="scope">
          <el-tag :type="statusType(scope.row.status)">
            {{scope.row.status}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="80">
        <template #default="scope">
          <el-dropdown>
            <span class="el-dropdown-link">
              <i class="el-icon-more"></i>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>Edit</el-dropdown-item>
                <el-dropdown-item>Delete</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-footer">
      <span>Showing {{pageStart + 1}}-{{pageEnd}} of {{users.length}} users</span>
      <el-pagination
          small
          background
          :current-page="page"
          :page-size="pageSize"
          :total="users.length"
          layout="prev, pager, next"
          @current-change="onPageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const users = ref([
  { username: 'johndoe', email: 'john.doe@example.com', membership: 'Premium', status: 'Active' },
  { username: 'janedoe', email: 'jane.doe@example.com', membership: 'Basic', status: 'Active' },
  { username: 'bobsmith', email: 'bob.smith@example.com', membership: 'Business', status: 'Pending' },
  // ...更多假数据
])
const search = ref('')
const page = ref(1)
const pageSize = 7

const filteredUsers = computed(() =>
    users.value.filter(u =>
        u.username.includes(search.value) ||
        u.email.includes(search.value)
    )
)
const pagedUsers = computed(() => filteredUsers.value.slice((page.value-1)*pageSize, page.value*pageSize))
const pageStart = computed(() => (page.value-1)*pageSize)
const pageEnd = computed(() => Math.min(page.value*pageSize, filteredUsers.value.length))

function onPageChange(val:number) { page.value = val }
function addUser() {
  ElMessage.info('添加用户弹窗演示')
}

function tagType(m: string) {
  if (m === 'Premium') return 'success'
  if (m === 'Business') return 'info'
  return 'default'
}
function statusType(s: string) {
  if (s === 'Active') return 'success'
  if (s === 'Pending') return 'warning'
  return 'info'
}
</script>

<style scoped>
.panel-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}
.user-table {
  margin-bottom: 0;
}
.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 13px;
  color: #999;
}
</style>
