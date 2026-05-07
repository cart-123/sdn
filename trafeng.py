from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3

class Traffic(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        m = ev.msg
        d = m.datapath
        p = d.ofproto_parser
        o = d.ofproto

        print("Traffic redirected to Port 2")

        # Action: Port 2-ku anupu
        a = [p.OFPActionOutput(2)]

        # PacketOut message
        out = p.OFPPacketOut(
            datapath=d,
            buffer_id=m.buffer_id,
            in_port=m.match['in_port'],
            actions=a,
            data=m.data if m.buffer_id == o.OFP_NO_BUFFER else None
        )
        d.send_msg(out)
