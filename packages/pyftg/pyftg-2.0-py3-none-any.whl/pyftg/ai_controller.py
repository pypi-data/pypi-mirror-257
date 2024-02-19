from threading import Thread

from .aiinterface.ai_interface import AIInterface
from .enum.flag import Flag
from .protoc import message_pb2, service_pb2, service_pb2_grpc
from .struct import (AudioData, FrameData, GameData, Key, RoundResult,
                     ScreenData)


class AIController(Thread):
    def __init__(self, stub: service_pb2_grpc.ServiceStub, ai: AIInterface, player_number: bool):
        Thread.__init__(self)
        self.stub = stub
        self.ai = ai
        self.player_number = player_number
    
    def initialize_rpc(self):
        request = service_pb2.InitializeRequest(player_number=self.player_number, player_name=self.ai.name(), is_blind=self.ai.is_blind())
        response = self.stub.Initialize(request)
        self.player_uuid: str = response.player_uuid

    def participate_rpc(self):
        request = service_pb2.ParticipateRequest(player_uuid=self.player_uuid)
        return self.stub.Participate(request)
    
    def input_rpc(self, key: Key):
        grpc_key = message_pb2.GrpcKey(A=key.A, B=key.B, C=key.C, U=key.U, D=key.D, L=key.L, R=key.R)
        self.stub.Input(service_pb2.PlayerInput(player_uuid=self.player_uuid, input_key=grpc_key))
    
    def run(self):
        self.initialize_rpc()
        for state in self.participate_rpc():
            flag = Flag(state.state_flag)
            if flag is Flag.INITIALIZE:
                self.ai.initialize(GameData(state.game_data), self.player_number)
            elif flag is Flag.PROCESSING:
                frame_data = FrameData(None if not state.HasField("frame_data") else state.frame_data)

                if state.HasField("non_delay_frame_data"):
                    self.ai.get_non_delay_frame_data(FrameData(state.non_delay_frame_data))

                self.ai.get_information(frame_data, state.is_control)

                if state.HasField("screen_data"):
                    self.ai.get_screen_data(ScreenData(state.screen_data))

                if state.HasField("audio_data"):
                    self.ai.get_audio_data(AudioData(state.audio_data))
                    
                self.ai.processing()
                self.input_rpc(self.ai.input())
            elif flag is Flag.ROUND_END:
                self.ai.round_end(RoundResult(state.round_result))
            elif flag is Flag.GAME_END:
                self.ai.round_end(RoundResult(state.round_result))
                self.ai.game_end()
