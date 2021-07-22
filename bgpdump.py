from mrtparse import *

class BgpDump:
    def __init__(self):
        self.as_path = []
        self.as4_path = []

    def save_neighbour_as(self, as_container):
        org_as_path = self.merge_as_path()
        as_path_list = []
        try:
            as_path_list = list(set(map(lambda asn: int(asn), org_as_path.split())))
        except ValueError:
            return

        # Skip the first AS
        for i in range(1, len(as_path_list)):
            curr_as = as_path_list[i]
            # Check if current AS is in the country
            if curr_as in as_container.country_as_list:

                # Check if neighbouring ASes are not in the country
                if i > 1:
                    prev_as = as_path_list[i-1]
                    if prev_as not in as_container.country_as_list:
                        as_container.as_dict[curr_as].add(prev_as)
                if i < len(as_path_list) - 1:
                    next_as = as_path_list[i+1]
                    if next_as not in as_container.country_as_list:
                        as_container.as_dict[curr_as].add(next_as)


    def td_v2(self, m, as_container):
        if (m['subtype'][0] == TD_V2_ST['RIB_IPV4_UNICAST']
            or m['subtype'][0] == TD_V2_ST['RIB_IPV4_MULTICAST']
            or m['subtype'][0] == TD_V2_ST['RIB_IPV6_UNICAST']
            or m['subtype'][0] == TD_V2_ST['RIB_IPV6_MULTICAST']):
            for entry in m['rib_entries']:
                self.as_path = []
                self.as4_path = []
                for attr in entry['path_attributes']:
                    self.bgp_attr(attr)
                self.save_neighbour_as(as_container)


    def bgp_attr(self, attr):
        if attr['type'][0] == BGP_ATTR_T['AS_PATH']:
            self.as_path = []
            for seg in attr['value']:
                if seg['type'][0] == AS_PATH_SEG_T['AS_SET']:
                    self.as_path.append('{%s}' % ','.join(seg['value']))
                elif seg['type'][0] == AS_PATH_SEG_T['AS_CONFED_SEQUENCE']:
                    self.as_path.append('(' + seg['value'][0])
                    self.as_path += seg['value'][1:-1]
                    self.as_path.append(seg['value'][-1] + ')')
                elif seg['type'][0] == AS_PATH_SEG_T['AS_CONFED_SET']:
                    self.as_path.append('[%s]' % ','.join(seg['value']))
                else:
                    self.as_path += seg['value']
        elif attr['type'][0] == BGP_ATTR_T['AS4_PATH']:
            self.as4_path = []
            for seg in attr['value']:
                if seg['type'][0] == AS_PATH_SEG_T['AS_SET']:
                    self.as4_path.append('{%s}' % ','.join(seg['value']))
                elif seg['type'][0] == AS_PATH_SEG_T['AS_CONFED_SEQUENCE']:
                    self.as4_path.append('(' + seg['value'][0])
                    self.as4_path += seg['value'][1:-1]
                    self.as4_path.append(seg['value'][-1] + ')')
                elif seg['type'][0] == AS_PATH_SEG_T['AS_CONFED_SET']:
                    self.as4_path.append('[%s]' % ','.join(seg['value']))
                else:
                    self.as4_path += seg['value']

    def merge_as_path(self):
        if len(self.as4_path):
            n = len(self.as_path) - len(self.as4_path)
            return ' '.join(self.as_path[:n] + self.as4_path)
        else:
            return ' '.join(self.as_path)

    def merge_aggr(self):
        if len(self.as4_aggr):
            return self.as4_aggr
        else:
            return self.aggr