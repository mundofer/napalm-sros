# Port values
Value Required description (.*)
Value interface (.\/.\/.|.\/.)
Value oper_speed (.*)
Value link_level (\S+)
Value config_speed (.*)
Value admin_state (\S+)
Value oper_duplex (\S+)
Value oper_state (\S+)
Value config_duplex (\S+)
Value physical_link (\S+)
Value MTU (\d*)
Value single_fiber_mode (\S+)
Value min_frame_length (\d+)
Value ifindex (\d+)
Value hold_time_up (\d+)
Value last_state_change (..\/..\/.... ..:..:..)
Value hold_time_down (\d+)
Value last_cleared_time (\S+)
Value ddm_events (\S+)
Value phys_state_chng_cnt (\d+)
Value configured_mode (\S+)
Value encap_type (\S+)
Value dot1q_ethertype (\S+)
Value qinq_ethertype (\S+)
Value pbb_ethertype (\S+)
Value ing_pool_rate (\d+)
Value egr_pool_rate (\d+)
Value ing_pool_policy (\S+)
Value egr_pool_policy (\S+)
Value net_egr_queue_pol (\S+)
Value egr_sched_pol (\S+)
Value monitor_port_sched (\S+)
Value monitor_agg_q_stats (\S+)
Value auto_negotiate (\S+)
Value mdi_mdx (\S+)
Value oper_phy_tx_clock (\S+)
Value accounting_policy (\S+)
Value collect_stats (\S+)
Value acct_plcy_eth_phys (\S+)
Value collect_eth_phys (\S+)
Value egress_rate (\S+)
Value ingress_rate (\S+)
Value load_balance_algo (\S+)
Value lacp_tunnel (\S+)
Value access_bandwidth (\S+)
Value booking_factor (\d+)
Value access_available_bw (\d+)
Value access_booked_bw (\d+)
Value sflow (\S+)
Value down_when_looped (\S+)
Value keep_alive (\d+)
Value loop_detected (\S+)
Value retry (\d+)
Value use_broadcast_addr (\S+)
Value sync_status_msg (\S+)
Value rx_quality_level (\S+)
Value tx_dus_dnu (\S+)
Value tx_quality_level (\S+)
Value ssm_code_type (\S+)
Value down_on_int_error (\S+)
Value doie_tx_disable (\S+)
Value crc_mon_sd_thresh (\S+)
Value crc_mon_window (\d+)
Value crc_mon_sf_thresh (\S+)
Value efm_oam (\S+)
Value efm_oam_link_mon (\S+)
Value configured_address (..:..:..:..:..:..)
Value hardware_address (..:..:..:..:..:..)

# Start of parse
Start
  # Record current values and change state.
  # No record will be output on first pass as 'Slot' is 'Required' but empty.
  ^Ethernet Interface -> Record Port

# reading values
Port
  ^Description\s+: ${description}
  ^Interface\s+: ${interface}\s+Oper Speed\s+:\s+${oper_speed}
  ^Link-level\s+: ${link_level}\s+Config Speed\s+: ${config_speed}
  ^Admin State\s+: ${admin_state}\s+Oper Duplex\s+: ${oper_duplex}
  ^Oper State\s+: ${oper_state}\s+Config Duplex\s+: ${config_duplex}
  ^Physical Link\s+: ${physical_link}\s+MTU\s+: ${MTU}
  ^Single Fiber Mode\s+: ${single_fiber_mode}\s+Min Frame Length\s+: ${min_frame_length} Bytes
  ^IfIndex\s+: ${ifindex}\s+Hold time up\s+: ${hold_time_up} seconds
  ^Last State Change\s*: ${last_state_change}\s+Hold time down\s+: ${hold_time_down} seconds
  ^Last Cleared Time\s*: ${last_cleared_time}\s+DDM Events\s+: ${ddm_events}
  ^Phys State Chng Cnt: ${phys_state_chng_cnt}
  ^Configured Mode\s*: ${configured_mode}\s*Encap Type\s*: ${encap_type}
  ^Dot1Q Ethertype\s*: ${dot1q_ethertype}\s*QinQ Ethertype\s*: ${qinq_ethertype}
  ^PBB Ethertype\s*: ${pbb_ethertype}
  ^Ing\. Pool \% Rate\s*: ${ing_pool_rate}\s*Egr\. Pool \% Rate\s*: ${egr_pool_rate}
  ^Ing\. Pool Policy\s*: ${ing_pool_policy}
  ^Egr\. Pool Policy\s*: ${egr_pool_policy}
  ^Net\. Egr\. Queue Pol\s*: ${net_egr_queue_pol}
  ^Egr\. Sched\. Pol\s*: ${egr_sched_pol}
  ^Monitor Port Sched\s*: ${monitor_port_sched}
  ^Monitor Agg Q Stats\s*: ${monitor_agg_q_stats}
  ^Auto-negotiate\s*: ${auto_negotiate}\s*MDI\/MDX\s*: ${mdi_mdx}
  ^Oper Phy-tx-clock\s*: ${oper_phy_tx_clock}
  ^Accounting Policy\s*: ${accounting_policy}\s*Collect-stats\s*: ${collect_stats}
  ^Acct Plcy Eth Phys\s*: ${acct_plcy_eth_phys}\s*Collect Eth Phys\s*: ${collect_eth_phys}
  ^Egress Rate\s*: ${egress_rate}\s*Ingress Rate\s*: ${ingress_rate}
  ^Load-balance-algo\s*: ${load_balance_algo}\s*LACP Tunnel\s*: ${lacp_tunnel}
  ^Access Bandwidth\s*: ${access_bandwidth}\s*Booking Factor\s*: ${booking_factor}
  ^Access Available BW\s*: ${access_available_bw}
  ^Access Booked BW\s*: ${access_booked_bw}
  ^Sflow\s*: ${sflow}
  ^Down-when-looped\s*: ${down_when_looped}\s*Keep-alive\s*: ${keep_alive}
  ^Loop Detected\s*: ${loop_detected}\s*Retry\s*: ${retry}
  ^Use Broadcast Addr\s*: ${use_broadcast_addr}
  ^Sync\. Status Msg\.\s*: ${sync_status_msg}\s*Rx Quality Level\s*: ${rx_quality_level}
  ^Tx DUS\/DNU\s*: ${tx_dus_dnu}\s*Tx Quality Level\s*: ${tx_quality_level}
  ^SSM Code Type\s*: ${ssm_code_type}
  ^Down On Int\. Error\s*: ${down_on_int_error}\s*DOIE Tx Disable\s*: ${doie_tx_disable}
  ^CRC Mon SD Thresh\s*: ${crc_mon_sd_thresh}\s*CRC Mon Window\s*: ${crc_mon_window} seconds
  ^CRC Mon SF Thresh\s*: ${crc_mon_sf_thresh}
  ^EFM OAM\s*: ${efm_oam}\s*EFM OAM Link Mon\s*: ${efm_oam_link_mon}
  ^Configured Address\s*: ${configured_address}
  ^Hardware Address\s*: ${hardware_address} -> Start