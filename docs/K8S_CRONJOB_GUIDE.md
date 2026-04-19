# VecAlpha 策略排行榜 K8s 自动化调度指南

本文档记录了基于 Docker Desktop (K8s) 环境的策略排行榜自动更新架构。为了优化资源利用率并提升长周期回测的稳定性，系统采用了**分级错峰调度**的设计。

## 1. 架构设计思路

由原先的单任务顺序执行模式，调整为多任务并行解耦模式：
- **短周期 (1w, 1m)**：更新频率高，资源占用少。
- **中周期 (3m)**：更新频率中等，资源占用中等。
- **长周期 (6m, 1y)**：更新频率低，数据量极大，资源占用高，需长时间运行。

通过拆分 CronJob，实现了：
1. **任务隔离**：某个时段任务失败不影响其他时段。
2. **资源优化**：针对不同数据量级分配差异化的 CPU 和内存限制。
3. **避免死锁**：通过时间错峰，解决共享 PVC (strategy-pvc) 的读写冲突。

## 2. 任务详情表

所有任务运行于 `quantrading` 命名空间，共享 `strategy-pvc` 存储。

| 任务名称 (CronJob) | 考察周期 | 执行频率 | 调度时间 (Vancouver) | CPU (Req/Lim) | 内存 (Req/Lim) | 超时限制 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `leaderboard-daily` | 1w, 1m | 每天一次 | 12:20 | 1C / 2C | 2G / 4G | 1 小时 |
| `leaderboard-3m` | 3m | 每二、五 | 02:00 | 1.5C / 2.5C | 4G / 6G | 2 小时 |
| `leaderboard-6m` | 6m | 每周六 | 02:00 | 2C / 3C | 6G / 8G | 4 小时 |
| `leaderboard-1y` | 1y | 每月 1 号 | 06:00 | 3C / 4C | 8G / 10G | 8 小时 |

## 3. 部署与维护

### 3.1 首次部署
```bash
# 进入项目根目录
kubectl apply -f deploy/k3s/cronjobs-multi-period.yaml
```

### 3.2 常用维护命令

**查看任务状态：**
```bash
kubectl get cronjob -n quantrading
```

**手动立即触发某个任务（例如 1y 更新）：**
```bash
# 创建一个单次运行的任务副本
kubectl create job --from=cronjob/leaderboard-1y manual-1y-run -n quantrading
```

**查看实时运行日志：**
```bash
# 首先找到对应的 Pod
kubectl get pods -n quantrading | grep leaderboard
# 查看日志
kubectl logs -f <POD_NAME> -n quantrading
```

### 3.3 挂起与恢复

如果需要临时停止所有自动化任务：
```bash
# 挂起每日任务
kubectl patch cronjob leaderboard-daily -n quantrading -p '{"spec" : {"suspend" : true}}'
```

恢复任务：
```bash
kubectl patch cronjob leaderboard-daily -n quantrading -p '{"spec" : {"suspend" : false}}'
```

## 4. 注意事项

1. **镜像更新**：建议定期更新 `neozhou2009/freqtrade-full:latest` 镜像，并将 `psycopg2-binary` 等依赖固化到 Dockerfile 中，以减少 Job 启动时的预热时间。
2. **PVC 空间**：长周期回测会下载大量 `.feather` 数据文件。目前 `strategy-pvc` 配置为 10Gi，若运行 1y 任务频率增加，需监控并考虑扩容。
3. **资源预留**：`leaderboard-1y` 任务峰值会占用约 4 核 CPU，执行时请确保 Docker Desktop 分配的总资源充足（建议分配 8 或 12 核给 Docker）。
